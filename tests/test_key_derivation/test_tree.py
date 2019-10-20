from key_derivation.tree import (
    flip_bits,
    IKM_to_lamport_SK,
    HKDF_mod_r,
    derive_master_SK,
    derive_child_SK,
)
from json import load

with open('tests/test_key_derivation/key_derivation_test_vectors.json', 'r') as f:
    test_vector = load(f)


def test_flip_bits():
    test_vector_int = int(test_vector['seed'][:64], 16)  # 64 comes from string chars containing .5 bytes
    assert test_vector_int & flip_bits(test_vector_int) == 0


def test_IKM_to_lamport_SK():
    test_vector_lamport_0 = [bytes.fromhex(x) for x in test_vector['lamport_0']]
    test_vector_lamport_1 = [bytes.fromhex(x) for x in test_vector['lamport_1']]
    IKM = test_vector['intermidiate_SK'].to_bytes(32, 'big')
    lamport_0 = IKM_to_lamport_SK(IKM=IKM, index=0)
    not_IKM = flip_bits(test_vector['intermidiate_SK']).to_bytes(32, 'big')
    lamport_1 = IKM_to_lamport_SK(IKM=not_IKM, index=0)
    assert test_vector_lamport_0 == lamport_0
    assert test_vector_lamport_1 == lamport_1


def test_HKDF_mod_r():
    test_0 = (bytes.fromhex(test_vector['seed']), test_vector['intermidiate_SK'])
    test_1 = (bytes.fromhex(test_vector['compressed_lamport_PK']), test_vector['SK'])
    for test in (test_0, test_1):
        assert HKDF_mod_r(IKM=test[0]) == test[1]


def test_derive_child_SK():
    test_parent_SK = test_vector['intermidiate_SK']
    test_SK = test_vector['SK']
    assert derive_child_SK(parent_SK=test_parent_SK, index=0) == test_SK


def test_derive_master_SK():
    test_seed = bytes.fromhex(test_vector['seed'])
    test_SK = test_vector['SK']
    assert derive_master_SK(test_seed) == test_SK