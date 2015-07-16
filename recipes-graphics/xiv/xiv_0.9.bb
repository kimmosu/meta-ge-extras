DESCRIPTION = "xiv is a lightweight simple image viewer for Linux"
HOMEPAGE = "http://xiv.sourceforge.net/"
LICENSE = "BSD"
LIC_FILES_CHKSUM = "file://COPYRIGHT;md5=daa273295f57ee294a0006e06131b4ad"

SRC_URI = "http://downloads.sourceforge.net/project/xiv/xiv-0.9.tgz"
SRC_URI[md5sum] = "83f86c2071b97d15c52f404f1947c2d4"
SRC_URI[sha256sum] = "9eeb295ec640f09681f7b21ac045aaf7144d5d3b417f8d4c301bfa3887d9527c"

S = "${WORKDIR}/xiv-${PV}"

DEPENDS = "virtual/libx11 jpeg tiff libexif"
RDEPENDS_${PN} += "bash"

# NOTE: if this software is not capable of being built in a separate build directory
# from the source, you should replace autotools with autotools-brokensep in the
# inherit line
inherit autotools-brokensep

# Specify any options you want to pass to the configure script using EXTRA_OECONF:
EXTRA_OECONF = ""

do_install () {
    oe_runmake install PREFIX=${D}/usr
}

FILES_${PN} += "${datadir}/icons/ ${datadir}/icons/xiv.xpm"
