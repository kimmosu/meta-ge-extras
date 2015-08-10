SUMMARY = "Script to run ethernet loopback test"
LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Proprietary;md5=0557f9d92cf58f2ccdd50f62f8ac0b28"

SRC_URI = "file://ge-net-loopback-test.sh"

S = "${WORKDIR}"

inherit allarch

do_install() {
    install -d ${D}${bindir}
    install -m755 ${S}/ge-net-loopback-test.sh    ${D}${bindir}
}

RDEPENDS_${PN} = "iperf iptables net-tools"
