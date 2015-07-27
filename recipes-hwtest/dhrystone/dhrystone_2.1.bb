SUMMARY = "Dhrystone CPU benchmark"
LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Proprietary;md5=0557f9d92cf58f2ccdd50f62f8ac0b28"

SRC_URI = "http://www.netlib.org/benchmark/dhry-c;downloadfilename=dhry-c.shar \
           file://dhrystone.patch"

SRC_URI[md5sum] = "75aa5909c174eed98c134be2f56307da"
SRC_URI[sha256sum] = "038a7e9169787125c3451a6c941f3aca5db2d2f3863871afcdce154ef17f4e3e"

do_unpack() {
    cd ${S}
    sh ${DL_DIR}/dhry-c.shar
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${S}/dhry ${D}${bindir}
}
