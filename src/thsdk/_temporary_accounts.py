from __future__ import annotations

from secrets import choice


_TEMPORARY_ACCOUNT_PREFIX = "thsguest_"

_TEMPORARY_ACCOUNT_ITEMS = [
    ("n35365t7", "29e9075556b7bcee6ecbc1e31e3d9bc6", "1a:6e:20:a4:6e:2d"),
    ("bqjbsllb", "f56c6a37055c326a578560b08df566fd", "aa:d0:98:7b:b3:72"),
    ("0a7mzp30", "7dfe8790d60753fb494513923423ec41", "ce:75:ca:83:b8:2b"),
    ("c3olb9gc", "f312b28edea08673946c8f56abd6bf5a", "be:76:8e:b8:44:60"),
    ("dv4u6hvp", "2dbba40ca63fef29bf3e6e6e151ae372", "f6:0f:3f:21:36:3c"),
    ("wp5sv42z", "93836975f5a34c2eff4cab58f3c38403", "4e:7e:41:2d:b2:37"),
    ("wziz9v4n", "a82f6ff964fc44c521cc6b64812c8302", "b6:13:49:9c:bf:51"),
    ("kj01qfgv", "6d014d319b3d77226c6b71ffeeec6874", "da:a0:f7:b6:1e:59"),
    ("6au8e9b5", "84d4fdb63f6a695807f0d1a84237a8f5", "12:88:f0:c6:a2:a8"),
    ("9n9wjhvo", "db484794d4c4cc8911ea3bae4d453b43", "56:9e:7a:fb:4a:0f"),
    ("kw5m3tki", "18740ee6393757bd859365d0dd5dbe38", "ca:e8:b7:f7:be:da"),
    ("ej3ehnvi", "3f153b438c57708820d132617c7610a3", "be:30:03:ed:19:fc"),
    ("k8wv0s2f", "95e0a73c13fe014e75a149ea3502fcb2", "32:35:74:d7:8a:64"),
    ("d65x5hzv", "4a8c784f9840f6bc4876e496aac2fa43", "62:0c:6f:fd:b0:da"),
    ("k5tyyg1f", "e0ae1f8471ed15edaec9536a72d59ed9", "76:86:d3:50:11:64"),
    ("u2erkssi", "9b1ee153efc91dccd04ea0b7263273bc", "da:5b:41:37:50:a9"),
    ("pqz6sv2x", "78d657f72e6b49cb455f54ed1dd57d46", "ce:19:82:e9:23:07"),
    ("app4n2nm", "f9de1e9bf13021649193e34b53045423", "7a:4b:bd:f3:0e:3d"),
    ("t529muay", "95d5de6a62567a5d45c7b25813d9cbda", "2a:2c:c6:ef:61:80"),
    ("1ssvi1v1", "98de0199e3f6de67598534910b64d8c6", "9e:ad:c1:2f:54:6b"),
    ("6hzj3cfa", "6f89aa71eaa65a7cb495352f0a0e7143", "8a:39:95:e0:02:b9"),
    ("oimmqml7", "d568efbec2021c42c7eda067991e6b32", "96:9c:6c:74:e3:3a"),
    ("kh04ek6q", "309caa162d3c27f199708fa441ecd9ad", "32:5e:d2:e2:d8:9f"),
    ("pw05sieq", "fe66dd87a8eae670beac40c392d1db92", "a2:19:96:31:aa:28"),
    ("bk278v3f", "9d6ea7614482cee9729d46854226b922", "9e:01:9f:da:66:1b"),
    ("janrnkle", "4849fd68536c76c878c38322c41cca22", "d2:df:c5:04:58:0f"),
    ("i4bxskin", "bb8f3baff00ff7e1ba86aa3eb97a1e30", "2e:60:90:c2:73:f6"),
    ("jdburol4", "97e04fb49f10b5bc69706c8bba8446f7", "2a:fd:6e:37:b1:8f"),
    ("9nlfe5k2", "efc8397212a8fe81c5a33fa6c9abf129", "5a:ca:57:da:9f:6e"),
    ("n7g33cl2", "83900f0cbee955c90ea9d9e13f7826a1", "3e:0e:02:d7:22:0f"),
    ("mxxwrsaz", "9514c00bb7f074754e84f9b5471ac179", "22:ee:12:08:3c:ac"),
    ("h1vthg4t", "04728d0a3e05630ac90f910befadce1b", "92:b8:41:78:f2:08"),
    ("jnkp1idy", "6e3b612cc850b8f3f3d4175fd7b1f66b", "02:03:20:e0:d4:ad"),
    ("fli7o75j", "ceeae4ccf8400d0846e0120805ffdf05", "f2:9d:22:31:ad:7c"),
    ("qkjxeizl", "fc1bd7c0e3fa5ca2a2c6ebcb994f7a17", "a2:be:8d:d5:eb:89"),
    ("0xwl0aow", "c1a110795b6befc80d3cdc9806a86ce2", "b6:8b:b1:ee:61:e3"),
    ("7fe73p4d", "18c7c0e2e374aa2ab6dab0c3b0ec579a", "4e:c1:50:4f:42:d7"),
    ("biqspra8", "d288dd117a9e27e32cb8d65d4148c24a", "86:d6:14:2f:af:5b"),
    ("w6ykyu6p", "93a01039fd9a75bb1f43d48145a77dfa", "72:c1:92:58:6a:5a"),
    ("r86k0wdm", "8aaa9816a8c3b680b595aaf056bee173", "66:5f:74:1f:9d:5e"),
    ("1wlbx4cb", "b996b1e1055cb993dccb5c2265fc6c80", "ea:32:a4:55:3c:09"),
    ("iy9v7m4o", "ed4f93815286a4483c66a3f8ad681008", "9a:ee:45:ed:61:aa"),
    ("8rynr5b0", "4f26ac218142808b2969032a13c59c73", "0a:91:eb:fe:81:42"),
    ("ejpx9bmk", "cbfc2fbf859313346d144513f3903af2", "62:bf:8c:5c:5d:2b"),
    ("rxptkeeg", "e6646287ad046caec8e29a4963e92584", "9e:e0:f2:b4:55:9c"),
    ("ykrjfiep", "086c32e44a03ba13473a872da9f8fbe0", "8a:3f:b4:39:4f:cb"),
    ("yy8jdkcz", "3465e2115a7851ad8907344701b5251e", "72:25:2a:82:b7:41"),
    ("a4xrcic5", "a4564ccf016a49f087a4ba7a0af02259", "92:a4:94:82:f0:71"),
    ("fw4bsnci", "a75cd7d25f7cd483581928afa31561bc", "1a:12:cb:ef:f8:a3"),
    ("umwll2l8", "d303706ccd2c73bf18c10a62d6bde40c", "fe:a3:15:5e:46:f2"),
    ("nbvb4mm8", "a16ea5fd49e863f69541d86ecb435221", "86:50:8f:e1:29:2b"),
    ("nhhlgmko", "3a89a06d44b55f39919306dad0ddc6c6", "0a:21:a1:57:e9:48"),
]


def acquire_temporary_account() -> tuple[str, str, str]:
    """Return one bundled temporary account for short-lived evaluation use."""
    suffix, password, mac = choice(_TEMPORARY_ACCOUNT_ITEMS)
    return f"{_TEMPORARY_ACCOUNT_PREFIX}{suffix}", password, mac


__all__: list[str] = []

