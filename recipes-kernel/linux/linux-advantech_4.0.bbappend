FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}-${PV}:"

SRC_URI += "file://defconfig \
            file://0001-gpio-generic-Add-hack-for-i.MX6-GPIO-reads.patch \
           "


