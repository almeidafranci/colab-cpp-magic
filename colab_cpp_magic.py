import os
import uuid
import timeit
import argparse
import tempfile
import subprocess
import IPython.core.magic as ipym

compiler = '/usr/bin/g++'
ext = '.cpp'


def get_argparser():
    parser = argparse.ArgumentParser(description='ColabCPPMagic params')
    parser.add_argument("-t", "--timeit", action='store_true',
                        help='flag to return timeit result instead of stdout')
    return parser


@ipym.magics_class
class ColabCPPMagic(ipym.Magics):

    def __init__(self, shell):
        super(ColabCPPMagic, self).__init__(shell)
        self.argparser = get_argparser()

    @staticmethod
    def compile(file_path):
        subprocess.check_output([compiler, file_path + ext, "-o", file_path + ".out", "-std=c++11"], stderr=subprocess.STDOUT)

    def run(self, file_path, timeit=False):
        if timeit:
            stmt = "subprocess.check_output(['{}'], stderr=subprocess.STDOUT)".format(file_path + ".out")
            output = self.shell.run_cell_magic(magic_name="timeit", line="-q -o import subprocess", cell=stmt)
        else:
            output = subprocess.check_output([file_path + ".out"], stderr=subprocess.STDOUT)
            output = output.decode('utf8')
        return output

    @ipym.cell_magic
    def cpp(self, line, cell):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, str(uuid.uuid4()))
            with open(file_path + ext, "w") as f:
                f.write(cell)
            try:
                self.compile(file_path)
                output = self.run(file_path, timeit=args.timeit)
            except subprocess.CalledProcessError as e:
                print(e.output.decode("utf8"))
                output = None
        return output


def load_ipython_extension(ip):
    colab_cpp_magic = ColabCPPMagic(ip)
    ip.register_magics(colab_cpp_magic)
