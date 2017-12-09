"""
Render all pdfs of the quiz.
"""

import pathlib
import subprocess
import shutil


pwd = pathlib.Path('.')
build_dir = pwd / "build"
build_dir.mkdir(exist_ok=True)
shutil.copy(str(pwd / "src/beamercolorthemesolarized.sty"), str(build_dir))



for tex_file in (pwd / "src").glob("*tex"):
    tex_code = tex_file.read_text(encoding="utf8")

    # Write solutions
    out_file = pathlib.Path(pwd / "build/{}.tex".format(tex_file.stem))
    out_file.write_text(tex_code, encoding="utf8")
    subprocess.call(["latexmk", "--xelatex", "-shell-escape", str(out_file.name)],
                    cwd = str(build_dir))
    shutil.copy(str(build_dir) + "/" + str(out_file.stem) + ".pdf", str(pwd / "solutions"))

    # Write questions
    out_file.write_text(tex_code.replace("Answer", "% Answer"), encoding="utf8")
    subprocess.call(["latexmk", "--xelatex", "-shell-escape", str(out_file.name)],
                    cwd = str(build_dir))
    shutil.copy(str(build_dir) + "/" + str(out_file.stem) + ".pdf", str(pwd / "questions"))

shutil.rmtree(str(build_dir))

