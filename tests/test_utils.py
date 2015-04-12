import unittest
import utils
import numpy as np


class TestUtils(unittest.TestCase):
    def test_top_sparse3(self):
        for beta in [1, 1.5, 2]:
            for factor in range(3):
                shape, rank, k, factors, x, x_indices, x_vals = \
                        utils.generate_dataset()
                model = utils.parafac(factors)

                # Generate the top numerator for the reference dense method
                einstr = utils.generate_dense(rank, factor)
                # Get all factors that aren't the current factor
                mode_factors = [a for j, a in enumerate(factors) if j != factor]
                mode_factors += [x * (model ** (beta - 2.)), ]
                top_d = np.einsum(einstr, *mode_factors)

                # Now get the top numerator for the sparse method
                top_s = np.zeros(factors[factor].shape, dtype=np.float32)
                utils.top_sparse3(x_indices, x_vals, top_s, beta, factor, *factors)

                result = np.allclose(top_d, top_s, rtol=1e-5)
                self.assertTrue(result)


    def test_bot_sparse3(self):
        for beta in [1, 1.5, 2]:
            for factor in range(3):
                shape, rank, k, factors, x, x_indices, x_vals = \
                        utils.generate_dataset()
                model = utils.parafac(factors)

                # Generate the bottom denominator for the reference dense method
                einstr = utils.generate_dense(rank, factor)
                # Get all factors that aren't the current factor
                mode_factors = [a for j, a in enumerate(factors) if j != factor]
                mode_factors += [(model ** (beta - 1.)), ]
                bot_d = np.einsum(einstr, *mode_factors)

                # Now get the bottom denominator for the sparse method
                bot_s = np.zeros(factors[factor].shape, dtype=np.float32)
                utils.bot_sparse3(x_indices, x_vals, bot_s, beta, factor, *factors)

                result = np.allclose(bot_d, bot_s, rtol=1e-5)
                self.assertTrue(result)


    def test_beta_divergence(self):
        shape, rank, k, factors, x, x_indices, x_vals = \
                utils.generate_dataset()
        for beta in [1, 1.5, 2]:
            a = x
            b = utils.parafac(factors)
            div_d = utils.beta_divergence_dense(a, b, beta)
            div_s = utils.beta_divergence(x_indices, x_vals, b, beta)
            div_s.shape = div_d.shape
            close = np.allclose(div_s, div_d, rtol=1e-5)
            self.assertTrue(close)
