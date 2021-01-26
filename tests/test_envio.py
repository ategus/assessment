import unittest
import envio
from click.testing import CliRunner

class envioTest(unittest.TestCase):

    def test_cli_param(self):

        runner = CliRunner()
        result = runner.invoke(
            envio.cli, '-i 3 -o 4'.split(), input='2')
        self.assertEqual(0, result.exit_code)
        self.assertIn("GPIOY(Input): 3 \nGPIOX(Output): 4", result.output)


    def test_cli_param_i_fail(self):

        runner = CliRunner()
        result = runner.invoke(
            envio.cli, '-o 3 '.split(), input='2')
        self.assertEqual(2, result.exit_code)
        self.assertIn("Usage: cli", result.output)
        

    def test_cli_param_o_fail(self):

        runner = CliRunner()
        result = runner.invoke(
            envio.cli, '-i 3 '.split(), input='2')
        self.assertEqual(2, result.exit_code)
        self.assertIn("Usage: cli", result.output)
        

    def test_cli_param_i_o_fail(self):

        runner = CliRunner()
        result = runner.invoke(envio.cli)
        self.assertEqual(2, result.exit_code)
        self.assertIn("Usage: cli", result.output)




if __name__ == '__main__' :
    unitest.main()
