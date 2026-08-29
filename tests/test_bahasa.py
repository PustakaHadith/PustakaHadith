"""Ujian Fasa 2: utils.bahasa.betulkan_melayu / simbol_boleh_dipapar."""
import utils.bahasa as b


def test_betulkan_melayu_kosong():
    assert b.betulkan_melayu("") == ""


def test_betulkan_melayu_pulangan_str():
    assert isinstance(b.betulkan_melayu("satu dua tiga"), str)


def test_betulkan_melayu_idempoten():
    # Sapaan dua kali mesti sama dengan sekali (tiada ayunan ejaan).
    sampel = "Nabi bersabda tentang shalat dan zakat serta puasa."
    sekali = b.betulkan_melayu(sampel)
    assert b.betulkan_melayu(sekali) == sekali


# Nota: simbol_boleh_dipapar() memanggil QFontMetrics yang MEMERLUKAN
# QApplication hidup — akan native-crash dalam ujian headless (tanpa paparan).
# Ia diuji secara manual dalam app sebenar, bukan di sini.
