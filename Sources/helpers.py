from matplotlib import pyplot as plt
from collections import Counter
import random
import secrets
import numpy as np
import qrng

# TODO: plot distributions for comparison, general testing
# test different np.random.Generator


def compute_prob(numbers, samples):
    dist = [Counter(numbers).get(x) for x in range(1, 7)]
    prob = [x / samples for x in dist]
    return prob


def compute_msq(dist):
    msq = 0
    for x in dist:
        msq += (1 / 6 - x) * (1 / 6 - x)
    return msq


def rnd_randint(x):
    return np.random.randint(1, 6 + 1, size=x)


def rnd_random(x):
    return np.ceil(np.random.random(x) * 6)


def rnd_rand(x):
    return np.ceil(np.random.rand(x) * 6)


def rnd_default_rng(x):
    return np.ceil(np.random.default_rng().random(x) * 6)


def rnd_system_random(x):
    return [np.ceil(random.SystemRandom().random() * 6) for _ in range(x)]


def rnd_secrets(x):
    return [secrets.SystemRandom().randint(1, 6) for _ in range(x)]


def rnd_qrng(x):
    return [qrng.get_random_int(1, 6) for _ in range(x)]


def __test():
    samples = 50
    steps = [1, 2, 3, 4, 5, 6]

    f = open("../Ressources/ibmq_cred.txt")
    ibmq_cred = f.read()
    qrng.set_provider_as_IBMQ(ibmq_cred)
    qrng.set_backend('ibmq_london')
    # qrng.set_backend('qasm_simulator')

    # Random Generators ---------------------------------------------
    # random.randint
    rnd1 = rnd_randint(samples)
    prob1 = compute_prob(rnd1)

    # random.random
    rnd2 = rnd_random(samples)
    prob2 = compute_prob(rnd2)

    # random.rand
    rnd3 = rnd_rand(samples)
    prob3 = compute_prob(rnd3)

    # random.SystemRandom
    rnd4 = rnd_system_random(samples)
    prob4 = compute_prob(rnd4)

    # secrets
    rnd5 = rnd_secrets(samples)
    prob5 = compute_prob(rnd5)

    # random.default.rng
    rnd6 = rnd_default_rng(samples)
    prob6 = compute_prob(rnd6)

    # qrng
    rnd7 = rnd_qrng(samples)
    prob7 = compute_prob(rnd7)

    # Plot -----------------------------------------------------------

    plt.style.use('default')
    plt.figure()
    ax = plt.axes()

    # distribution

    plt.plot(steps, prob1, label='$random.randint$')
    plt.plot(steps, prob2, label='$random.random$')
    plt.plot(steps, prob3, label='$random.rand$')
    plt.plot(steps, prob4, label='$random.SystemRandom.random$')
    plt.plot(steps, prob5, label='$random.default-rng$')
    plt.plot(steps, prob6, label='$secrets.SystemRandom.randint$')
    plt.plot(steps, prob7, label='$qrng$')

    plt.legend()
    ax.set_xlabel('dice result')
    ax.set_ylabel('probability')
    ax.set_title('Probability distribution of different RNGs')
    plt.show()

    print('== msq ==')
    print(f'{compute_msq(prob1):.10f}', 'random.randint')
    print(f'{compute_msq(prob2):.10f}', 'random.random')
    print(f'{compute_msq(prob3):.10f}', 'random.rand')
    print(f'{compute_msq(prob4):.10f}', 'random.SystemRandom.random')
    print(f'{compute_msq(prob5):.10f}', 'random.default-rng')
    print(f'{compute_msq(prob6):.10f}', 'secrets.SystemRandom.randint')
    print(f'{compute_msq(prob7):.10f}', 'qrng')
