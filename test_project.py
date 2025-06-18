import pytest
import sqlite3
from project import normalize_text
from project import extract_province2
from project import dst_by_type
from project import most_freq_dst
from project import dst_by_prov


def test_remove_accents():
    assert normalize_text("Quảng Ninh") == "Quang Ninh"
    assert normalize_text("Quảng     Ninh    ") == "Quang Ninh"
    assert normalize_text("quảng NINH") == "Quang Ninh"
    assert normalize_text("quảng ninh") == "Quang Ninh"


def test_extract_province2():
    assert extract_province2("Xã Ngọk Tem - huyện Kon Plông - tỉnh Kon Tum") == "Kon Tum"
    assert extract_province2("Xã Thanh Chăn - huyện Điện Biên - tỉnh Điện Biên") == "Đien Bien"
    assert extract_province2('"Phường Thới Long, Long Hưng - quận Ô Môn - TP.Cần Thơ"') == "Can Tho"
    assert extract_province2('"Xã Nâm N\'Dir huyện Krông Nô, xã Đắk Gằn huyện Đăk Mi, tỉnh Đăk Nông"') == "Đak Nong"
    assert extract_province2('"Phường Châu Văn Liêm, quận Ô Môn, thành phố Cần Thơ"') == "Can Tho"
    assert extract_province2("Các tỉnh/tp khu vực Bắc Bộ và Bắc Trung Bộ") == "Khu Vuc Bac Bo Va Bac Trung Bo"


def test_dst_by_type():
    cnn = sqlite3.connect("vieDisasters.db")
    db = cnn.cursor()

    db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" GROUP BY "type" ORDER BY "count" DESC')
    dbtype = db.fetchall()
    assert len(dst_by_type(db, "vie", 1)) == len(dbtype)
    assert dst_by_type(db, "vie", 1)[0][1] == dbtype[0][1]
    db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" GROUP BY "type" ORDER BY "count"')
    dbtype = db.fetchall()
    assert dst_by_type(db, "vie", 0)[0][1] == dbtype[0][1]

    db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" WHERE "province" = "Quang Ninh" GROUP BY "type" ORDER BY "count"')
    quangninh = db.fetchall()
    assert len(dst_by_type(db, "Quang Ninh", 0)) == len(quangninh)
    assert dst_by_type(db, "Quang Ninh", 0)[0][1] == quangninh[0][1]
    db.execute('SELECT "type", COUNT("index") AS "count" FROM "disasters" WHERE "province" = "Quang Ninh" GROUP BY "type" ORDER BY "count" DESC')
    quangninh = db.fetchall()
    assert dst_by_type(db, "Quang Ninh", 1)[0][1] == quangninh[0][1]

    with pytest.raises(KeyError):
        dst_by_type(db, "abc", 0)
    with pytest.raises(KeyError):
        dst_by_type(db, 1, 0)
    
    cnn.close()


def test_most_freq_dst():
    cnn = sqlite3.connect("vieDisasters.db")
    db = cnn.cursor()

    db.execute('SELECT "type", "count" FROM (SELECT "type", COUNT("type") AS "count" FROM "disasters" GROUP BY "type") WHERE ("count" = (SELECT MAX("count") FROM (SELECT COUNT("type") AS "count" FROM "disasters" GROUP BY "type")))')
    most_vie = db.fetchall()
    assert len(most_freq_dst(db, "vie")) == len(most_vie)
    assert most_freq_dst(db,"vie")[0][1] == most_vie[0][1]

    db.execute('SELECT "type", "count" FROM (SELECT "type", COUNT("type") AS "count" FROM "disasters" WHERE "province" = "Ha Noi" GROUP BY "type") WHERE ("count" = (SELECT MAX("count") FROM (SELECT COUNT("type") AS "count" FROM "disasters" WHERE "province" = "Ha Noi" GROUP BY "type")))')
    hanoi = db.fetchall()
    assert len(most_freq_dst(db, "Ha Noi")) ==  len(hanoi)
    assert most_freq_dst(db, "Ha Noi")[0][1] == hanoi[0][1]

    with pytest.raises(KeyError):
        most_freq_dst(db, "abc")
    
    cnn.close()


def test_dst_by_prov():
    cnn = sqlite3.connect("vieDisasters.db")
    db = cnn.cursor()

    db.execute('SELECT "province", COUNT("province") AS "count" FROM "disasters" GROUP BY "province" ORDER BY "count" DESC')
    full = db.fetchall()
    assert len(dst_by_prov(db, 5, 0)) <= 5
    assert len(dst_by_prov(db, 0, 0)) == len(full)
    assert len(dst_by_prov(db, 5, 1)) <= 5
    assert len(dst_by_prov(db, 0, 1)) == len(full)

    assert dst_by_prov(db, 5, 1)[0][1] == full[0][1]
    assert dst_by_prov(db, 5, 0)[0][1] == full[-1][1]

    with pytest.raises(ValueError):
        dst_by_prov(db, "A", 0)
    with pytest.raises(ValueError):
        dst_by_prov(db, 1, "a")
    with pytest.raises(ValueError):
        dst_by_prov(db, 'a', 'a')
    with pytest.raises(ValueError):
        dst_by_prov(db, 1, 5)

    cnn.close()
    