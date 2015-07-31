SUMMARY = "Read temperature and pressure from MPL3115"
LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Proprietary;md5=0557f9d92cf58f2ccdd50f62f8ac0b28"

SRC_URI = "file://ge-temp-logger.py"

S = "${WORKDIR}"

inherit allarch


do_install() {
    install -d ${D}${bindir}
    install -m644 ${S}/ge-temp-logger.py    ${D}${bindir}
}

RDEPENS = "python"