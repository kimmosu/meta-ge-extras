DESCRIPTION = "Linpack benchmark"
HOMEPAGE = "http://www.netlib.org/benchmark/linpackc.new"

LICENSE = "Proprietary"
LIC_FILES_CHKSUM = "file://linpack.c;md5=1c5d0b6a31264685d2e651c920e3cdf4"

SRC_URI = "http://www.netlib.org/benchmark/linpackc.new;downloadfilename=linpack.c"
SRC_URI[md5sum] = "1c5d0b6a31264685d2e651c920e3cdf4"
SRC_URI[sha256sum] = "a63f2ec86512959f1fd926bfafb85905b2d7b7402942ffae3af374d48745e97e"

do_unpack() {
    [ -d ${S} ] || mkdir -p ${S}
    cp ${DL_DIR}/linpack.c ${S}
}

do_compile() {
    ${CC} -O -o linpack linpack.c
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 linpack ${D}${bindir}
}
