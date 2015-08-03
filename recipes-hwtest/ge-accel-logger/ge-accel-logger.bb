SUMMARY = "Read accelerometer values from MMA8453"
LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Proprietary;md5=0557f9d92cf58f2ccdd50f62f8ac0b28"

SRC_URI = "file://ge-accel-logger.py"

S = "${WORKDIR}"

inherit allarch


do_install() {
    install -d ${D}${bindir}
    install -m755 ${S}/ge-accel-logger.py    ${D}${bindir}
}

RDEPENS = "python"
