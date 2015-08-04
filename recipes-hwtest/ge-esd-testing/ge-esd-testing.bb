SUMMARY = "Helper script for ESD tests"
LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Proprietary;md5=0557f9d92cf58f2ccdd50f62f8ac0b28"

SRC_URI = "file://ge-esd-testing.sh"

S = "${WORKDIR}"

inherit allarch


do_install() {
    install -d ${D}${bindir}
    install -m755 ${S}/ge-esd-testing.sh    ${D}${bindir}
}

#RDEPENDS_${PN} = "sh"
