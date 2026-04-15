import ctypes
import mmap
import time
import serial

# Serial port configuration
SERIAL_PORT = 'COM3'
BAUD_RATE = 9600

# Physics data structure
class SPageFilePhysics(ctypes.Structure):
    _fields_ = [
        ("packetId", ctypes.c_int),
        ("gas", ctypes.c_float),
        ("brake", ctypes.c_float),
        ("fuel", ctypes.c_float),
        ("gear", ctypes.c_int),
        ("rpm", ctypes.c_int),
        ("steerAngle", ctypes.c_float),
        ("speedKmh", ctypes.c_float),
    ]

# Graphics data structure
class SPageFileGraphic(ctypes.Structure):
    _pack_ = 4
    _fields_ = [
        ("packetId", ctypes.c_int),
        ("status", ctypes.c_int),
        ("session", ctypes.c_int),
        ("currentTime", ctypes.c_wchar * 15),
        ("lastTime", ctypes.c_wchar * 15),
        ("bestTime", ctypes.c_wchar * 15),
        ("split", ctypes.c_wchar * 15),
        ("completedLaps", ctypes.c_int),
        ("position", ctypes.c_int),
        ("iCurrentTime", ctypes.c_int),
        ("iLastTime", ctypes.c_int),
        ("iBestTime", ctypes.c_int),
        ("sessionTimeLeft", ctypes.c_float),
        ("distanceTraveled", ctypes.c_float),
        ("isInPit", ctypes.c_int),
        ("currentSectorIndex", ctypes.c_int),
        ("lastSectorTime", ctypes.c_int),
        ("numberOfLaps", ctypes.c_int),
    ]

# Static data structure
class SPageFileStatic(ctypes.Structure):
    _fields_ = [
        ("smVersion", ctypes.c_char * 15),
        ("acVersion", ctypes.c_char * 15),
        ("numberOfSessions", ctypes.c_int),
        ("numCars", ctypes.c_int),
        ("carModel", ctypes.c_char * 33),
    ]

# Parse lap time string (format "M:SS:mmm") to total seconds (float)
def safe_time_parse(time_str):
    try:
        if not time_str or time_str.strip() == '' or time_str == "0":
            return 0.0
        parts = time_str.strip().split(':')
        if len(parts) == 3:
            minutes = int(parts[0])
            seconds = int(parts[1])
            milliseconds = int(parts[2])
            total_seconds = minutes * 60 + seconds + milliseconds / 1000.0
            return total_seconds
        elif len(parts) == 2:
            minutes = int(parts[0])
            seconds = float(parts[1])
            return minutes * 60 + seconds
        else:
            return float(parts[0])
    except Exception:
        return 0.0

# Format seconds (float) back to "M:SS:mmm" string format
def format_lap_time(seconds):
    if seconds <= 0:
        return "0:00:000"
    minutes = int(seconds // 60)
    seconds_rem = int(seconds % 60)
    milliseconds = int(round((seconds - int(seconds)) * 1000))
    return f"{minutes}:{seconds_rem:02d}:{milliseconds:03d}"

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to {SERIAL_PORT} at {BAUD_RATE} baud.")

        mm_physics = mmap.mmap(-1, ctypes.sizeof(SPageFilePhysics), tagname="Local\\acpmf_physics", access=mmap.ACCESS_READ)
        mm_graphics = mmap.mmap(-1, ctypes.sizeof(SPageFileGraphic), tagname="Local\\acpmf_graphics", access=mmap.ACCESS_READ)
        mm_static = mmap.mmap(-1, ctypes.sizeof(SPageFileStatic), tagname="Local\\acpmf_static", access=mmap.ACCESS_READ)

        while True:
            mm_physics.seek(0)
            physics = SPageFilePhysics.from_buffer_copy(mm_physics.read(ctypes.sizeof(SPageFilePhysics)))
            speed = physics.speedKmh
            rpm = physics.rpm
            gear = physics.gear

            mm_graphics.seek(0)
            graphics = SPageFileGraphic.from_buffer_copy(mm_graphics.read(ctypes.sizeof(SPageFileGraphic)))
            best_time_raw = graphics.bestTime
            last_time_raw = graphics.lastTime
            distance = graphics.distanceTraveled
            position = graphics.position
            completed_laps = graphics.completedLaps
            session_time_left = graphics.sessionTimeLeft

            best_lap_sec = safe_time_parse(best_time_raw)
            last_lap_sec = safe_time_parse(last_time_raw)

            best_lap_str = format_lap_time(best_lap_sec)
            last_lap_str = format_lap_time(last_lap_sec)

            mm_static.seek(0)
            static = SPageFileStatic.from_buffer_copy(mm_static.read(ctypes.sizeof(SPageFileStatic)))
            car_model = static.carModel.decode('utf-8', errors='ignore').rstrip('\x00').strip()

            print(f"{car_model} | Speed: {speed:.1f} km/h | RPM: {rpm} | Gear: {gear} | Best Lap: {best_lap_str} | Last Lap: {last_lap_str} | Distance: {distance:.1f} m | Pos: {position} | Laps: {completed_laps} | Session left: {session_time_left:.1f}s")

            message = f"{car_model}|{rpm}|{speed:.1f}|{best_lap_str}|{last_lap_str}|{session_time_left:.1f}|{distance:.1f}|{completed_laps}|{position}|{gear}\n"
            ser.write(message.encode())

            time.sleep(0.1)

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    main()
