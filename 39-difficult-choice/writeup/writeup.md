Writeup
===

```
$ python vol.py -f ~/Desktop/chal.mem --profile=LinuxUbuntu_5_4_0-42-genericx64 linux_bash
Volatility Foundation Volatility Framework 2.6.1
Pid      Name                 Command Time                   Command
-------- -------------------- ------------------------------ -------
    2360 bash                 2021-08-25 05:52:37 UTC+0000   cd cd LiME/src/
    2360 bash                 2021-08-25 05:52:37 UTC+0000   ?%
    2360 bash                 2021-08-25 05:52:37 UTC+0000   cd LiME/src/
    2360 bash                 2021-08-25 05:52:37 UTC+0000   sudo insmod lime-5.4.0-42-generic.ko "path=/home/user/Desktop/chal.mem format=lime"
    2360 bash                 2021-08-25 05:52:37 UTC+0000   rm ~/.bash_history 
    2360 bash                 2021-08-25 05:52:57 UTC+0000   eog ~/Desktop/flag.jpg &
    2360 bash                 2021-08-25 05:53:10 UTC+0000   @
    2360 bash                 2021-08-25 05:53:10 UTC+0000   cd ~/LiME/src/
    2360 bash                 2021-08-25 05:53:18 UTC+0000   sudo insmod lime-5.4.0-42-generic.ko "path=/home/user/Desktop/chal.mem format=lime"



$ python vol.py -f ~/Desktop/chal.mem --profile=LinuxUbuntu_5_4_0-42-genericx64 linux_pslist  | grep eog
Volatility Foundation Volatility Framework 2.6.1
0xffff9925f4d92e80 eog                  2372            2360            1000            1000   0x0000000018a9c000 2021-08-25 05:53:00 UTC+0000


$ python vol.py -f ~/Desktop/chal.mem --profile=LinuxUbuntu_5_4_0-42-genericx64 linux_dump_map -p 2372 --dump-dir ~/Desktop/2372/
Volatility Foundation Volatility Framework 2.6.1
Task       VM Start           VM End                         Length Path
---------- ------------------ ------------------ ------------------ ----
      2372 0x000055de45b84000 0x000055de45b86000             0x2000 /home/user/Desktop/2372/task.2372.0x55de45b84000.vma
      2372 0x000055de45d85000 0x000055de45d86000             0x1000 /home/user/Desktop/2372/task.2372.0x55de45d85000.vma
      2372 0x000055de45d86000 0x000055de45d87000             0x1000 /home/user/Desktop/2372/task.2372.0x55de45d86000.vma
      2372 0x000055de479a6000 0x000055de48033000           0x68d000 /home/user/Desktop/2372/task.2372.0x55de479a6000.vma
      2372 0x00007fa270000000 0x00007fa270021000            0x21000 /home/user/Desktop/2372/task.2372.0x7fa270000000.vma
      2372 0x00007fa270021000 0x00007fa274000000          0x3fdf000 /home/user/Desktop/2372/task.2372.0x7fa270021000.vma
      2372 0x00007fa278000000 0x00007fa278021000            0x21000 /home/user/Desktop/2372/task.2372.0x7fa278000000.vma
      2372 0x00007fa278021000 0x00007fa27c000000          0x3fdf000 /home/user/Desktop/2372/task.2372.0x7fa278021000.vma


$ binwalk * | tee ../2372.log

$ binwalk task.2372.0x7fa27c000000.vma --dd=".*"

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
5376          0x1500          Unix path: /usr/share/pixmaps/nobody.png
6576          0x19B0          Unix path: /usr/share/pixmaps/transmission.xpm
11760         0x2DF0          Unix path: /usr/share/eog/icons
19024         0x4A50          Unix path: /usr/share/pixmaps/vim-16.xpm
20192         0x4EE0          Unix path: /usr/share/pixmaps/nohost.png
27488         0x6B60          Unix path: /home/user/.local/share/icons/ubuntu-mono-dark
31328         0x7A60          Unix path: /usr/share/ubuntu/icons/ubuntu-mono-dark
40624         0x9EB0          Unix path: /var/lib/snapd/desktop/pixmaps/gnome
42288         0xA530          Unix path: /usr/local/share/pixmaps/gnome
62688         0xF4E0          Unix path: /usr/share/pixmaps
65200         0xFEB0          Unix path: /usr/share/pixmaps/debian-logo.png
66832         0x10510         Unix path: /usr/share/icons/ubuntu-mono-dark/actions/16
67520         0x107C0         Unix path: /usr/share/icons/ubuntu-mono-dark/animations/24
68288         0x10AC0         Unix path: /usr/share/icons/ubuntu-mono-dark/apps/24
68560         0x10BD0         Unix path: /usr/share/icons/ubuntu-mono-dark/categories/22
83104         0x144A0         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders
85248         0x14D00         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-svg.so
94624         0x171A0         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-svg.so
108307        0x1A713         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-jpeg.so: undefined symbol: g_module_unload
111504        0x1B390         Unix path: /usr/share/icons/ubuntu-mono-dark/actions/24
118720        0x1CFC0         Unix path: /usr/share/icons/Humanity-Dark/places@2/16
132983        0x20777         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-jpeg.so: undefined symbol: g_module_check_init
146256        0x23B50         Unix path: /usr/share/icons/Adwaita/32x32/emotes
159808        0x27040         Unix path: /home/user/Desktop
179712        0x2BE00         Unix path: /usr/share/pixmaps/gdm-setup.png
237808        0x3A0F0         Unix path: /var/lib/snapd/desktop/icons/hicolor
243632        0x3B7B0         Unix path: /home/user/.local/share/icons/hicolor
246288        0x3C210         Unix path: /usr/share/pixmaps/gdm-xnest.png
247776        0x3C7E0         Unix path: /usr/share/icons/ubuntu-mono-dark/actions/24
251584        0x3D6C0         Unix path: /usr/share/icons/Humanity-Dark/apps/24
260032        0x3F7C0         Unix path: /usr/share/icons/Humanity-Dark/places/16
264848        0x40A90         Unix path: /usr/share/icons/Humanity-Dark/status/24
265008        0x40B30         Unix path: /usr/share/icons/ubuntu-mono-dark/status/24
265168        0x40BD0         Unix path: /usr/share/icons/Humanity/status/24
278720        0x440C0         Unix path: /usr/share/icons/Humanity/places@2/16
314368        0x4CC00         Unix path: /home/user/Desktop
335826        0x51FD2         Unix path: /home/user/Desktop/flag.jpg
359168        0x57B00         Unix path: /usr/share/pixmaps/hplj1020_icon.png
366240        0x596A0         Unix path: /usr/share/icons/Adwaita/16x16/emotes
368080        0x59DD0         Unix path: /usr/share/icons/Adwaita/22x22/devices
649360        0x9E890         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-svg.so
779392        0xBE480         Unix path: /home/user/Desktop
787536        0xC0450         Unix path: /usr/share/icons
789392        0xC0B90         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-jpeg.so
803920        0xC4450         Unix path: /usr/local/share/icons
889504        0xD92A0         Unix path: /usr/share/icons/Adwaita/16x16/actions
891152        0xD9910         Unix path: /usr/share/icons/hicolor/16x16/status
893463        0xDA217         Unix path: /usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/2.10.0/loaders/libpixbufloader-jpeg.so: undefined symbol: g_module_check_init
901888        0xDC300         Unix path: /usr/share/icons/hicolor/32x32/status
919504        0xE07D0         Unix path: /usr/share/icons/hicolor/256x256/apps
924224        0xE1A40         Unix path: /usr/share/icons/Adwaita/512x512/mimetypes
1038034       0xFD6D2         MySQL MISAM index file Version 3
1038440       0xFD868         MySQL MISAM index file Version 2
1038998       0xFDA96         MySQL MISAM compressed data file Version 4
1041696       0xFE520         MySQL MISAM index file Version 2
1050006       0x100596        MySQL MISAM index file Version 3
1053207       0x101217        MySQL MISAM index file Version 2
1054246       0x101626        MySQL ISAM compressed data file Version 3
1054699       0x1017EB        MySQL MISAM index file Version 3
1054936       0x1018D8        MySQL MISAM index file Version 3
1057912       0x102478        JPEG image data, JFIF standard 1.01

```

`0x102478` is the jpg containing the flag.

