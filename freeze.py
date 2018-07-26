import cx_Freeze

executables = [cx_Freeze.Executable("game.py")]

cx_Freeze.setup(
    name="Dr Darwin",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["/Users/cleye.jensen/Dropbox/Projects/Python/STEM/"]}},
    executables = executables
)