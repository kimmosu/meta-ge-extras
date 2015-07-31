SUMMARY = "Install GE video test files"
LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/files/common-licenses/Proprietary;md5=0557f9d92cf58f2ccdd50f62f8ac0b28"

SRC_URI = "http://hubblesource.stsci.edu/sources/video/clips/details/images/orion_2.mpg"

SRC_URI[md5sum] = "d4498ad77f53a81f555c4f9bca34c454"
SRC_URI[sha256sum] = "ae708b6f318fcd54ada16335a2b12e7f5aa5eedafae319a43ca652980676e9ba"

S = "${WORKDIR}"

inherit allarch

do_install() {
    install -d ${D}/usr/share/ge-video-test
    install -m644 ${S}/orion_2.mpg     ${D}/usr/share/ge-video-test
}

RDEPENDS_${PN} = "alsa-utils"
