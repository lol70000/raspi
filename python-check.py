import sys
import platform


# show informations about the current python version.
def show_python():
    print("python", sys.version)


# show informations about the platform.
def show_platform():
    print("platform.system:", platform.system())
    print("current platform:", platform.platform())
    print("platform machine:", platform.machine())
    print("platform version:", platform.version())


# Call the functions
print('informations about your current python & platform:')
print('')
show_python()
print('')
show_platform()
