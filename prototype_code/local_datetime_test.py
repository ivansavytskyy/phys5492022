from datetime import datetime
from datetime import timezone

time_object = datetime.now(tz=timezone.utc)
base_time = f"{time_object.hour:02}{time_object.minute:02}{time_object.second:02}"
decimal_time = f"{time_object.microsecond/1e6:.2}"
print(base_time + decimal_time[-3:])
pass