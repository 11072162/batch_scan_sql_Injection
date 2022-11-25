from tools import site
import time

start = time.time()
site()
end = time.time()
print(str(round(end - start, 3)) + 's')