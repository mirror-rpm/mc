Summary: A user-friendly file manager and visual shell.
Name:		mc
Version:	4.6.0
Release: 4
Epoch:          1
Copyright:	GPL
Group: System Environment/Shells
Source0:        http://www.ibiblio.org/pub/Linux/utils/file/managers/mc/mc-%{version}.tar.gz
Source1:	mc-cvs-uzip
URL:		http://www.ibiblio.org/mc/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	gpm-devel
BuildRequires:	slang

Prereq:		dev >= 3.3-3

Patch1:		mc-4.6.0-absoluterm.patch
Patch2:		mc-4.6.0-ptsname.patch
Patch3:		mc-4.6.0-stderr.patch
Patch4:		mc-4.6.0-troff.patch
Patch5:		mc-4.6.0-vcsa.patch
Patch6:		mc-4.6.0-pre3-nocpio.patch
Patch7:		mc-4.6.0-slang.patch
Patch8:		mc-4.6.0-utf8.patch

%description
Midnight Commander is a visual shell much like a file manager, only
with many more features. It is a text mode application, but it also
includes mouse support if you are running GPM. Midnight Commander's
best features are its ability to FTP, view tar and zip files, and to
poke into RPMs for specific files.

%prep
%setup -q -n mc-%{version}

cp -f %{SOURCE1} vfs/extfs

# Use /bin/rm, not rm
%patch1 -p1 -b .absoluterm

%patch2 -p1 -b .ptsname
%patch3 -p1 -b .stderr
%patch4 -p1 -b .troff

# new cons.saver
%patch5 -p1 -b .vcsa

# https://bugzilla.redhat.com/bugzilla/show_bug.cgi?id=78506
%patch6 -p1 -b .nocpio

# build with system slang
%patch7 -p1 -b .slang

# partially done UTF-8ization
%patch8 -p1 -b .utf8

%build
export CFLAGS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE $RPM_OPT_FLAGS"
%configure --sysconfdir=%{_sysconfdir} --with-screen=slang
make %{?_smp_mflags}

%install 
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

%{makeinstall} sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}

install lib/{mc.sh,mc.csh} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

# no longer works for 4.6.0, need to evaluate
## install -m 644 lib/mc.global $RPM_BUILD_ROOT%{_sysconfdir}

for I in /etc/pam.d/mcserv \
	/etc/rc.d/init.d/mcserv \
	/etc/mc.global; do
	rm -rf ${RPM_BUILD_ROOT}${I}
done

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(-, root, root)

%doc FAQ COPYING NEWS README
%{_bindir}/mc
%{_bindir}/mcedit
%{_bindir}/mcmfmt
%{_datadir}/mc/*
%attr(4711, vcsa, root) %{_libdir}/mc/cons.saver
%{_mandir}/man1/*
%config %{_sysconfdir}/profile.d/*
%dir %{_libdir}/mc

%changelog
* Mon Feb 24 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Feb 22 2003 Jakub Jelinek <jakub@redhat.com> 4.6.0-3
- second part of UTF-8ization

* Fri Feb 21 2003 Jakub Jelinek <jakub@redhat.com> 4.6.0-2
- kill unneeded patches, update the rest for 4.6.0
- build with system slang
- first part of UTF-8ization

* Fri Feb 14 2003 Havoc Pennington <hp@redhat.com> 4.6.0-1
- 4.6.0 final
- epoch 1 to work around 4.6.0pre > 4.6.0

* Thu Feb 13 2003 Havoc Pennington <hp@redhat.com> 4.6.0pre3-3
- drop our translations, they are surely out of date
- ugh, due to spec file weirdness hadn't actually used the new pre3
  tarball. disabled patches that no longer apply.
- patch for #78506

* Thu Feb 06 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- link also on mainframe against gpm-devel

* Tue Feb  4 2003 Havoc Pennington <hp@redhat.com> 4.6.0pre3-1
- pre3

* Tue Jan 28 2003 Havoc Pennington <hp@redhat.com>
- rebuild

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Fri Dec  6 2002 Havoc Pennington <hp@redhat.com>
- 4.6.0-pre1
- comment out the patches that don't apply, 
  if someone wants to spend time fixing them 
  that'd be great

* Mon Dec 02 2002 Elliot Lee <sopwith@redhat.com>
- Remove 'percent prep' in changelog
- Fix unpackaged files

* Fri Aug 23 2002 Karsten Hopp <karsten@redhat.de>
- fix german umlaut in menues (#68130)

* Fri Jul 19 2002 Jakub Jelinek <jakub@redhat.com> 4.5.55-11
- removed trailing backslash for %%configure, which
  caused mc to build with the buildroot prefix

* Wed Jul 17 2002 Karsten Hopp <karsten@redhat.de> 4.5.55-10
- support large files (#65159, #65160)
- own /usr/lib/mc/extfs and /usr/lib/mc/syntax
- fix NL translation (#63495)

* Thu Jul  4 2002 Jakub Jelinek <jakub@redhat.com>
- fix regex usage

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Fri Apr 12 2002 Havoc Pennington <hp@redhat.com>
- patch for trpm vfs, #62306

* Wed Apr 10 2002 Havoc Pennington <hp@redhat.com>
- don't build --with-included-slang on upstream recommendation
- add uzip method from cvs, fixes some sort of format string problem
- get fix for breaking zip files while browsing them from upstream

* Tue Apr  9 2002 Havoc Pennington <hp@redhat.com>
- remove bash-specific export from mc.sh

* Thu Mar 28 2002 Havoc Pennington <hp@redhat.com>
- cons.saver rewrite to use vcsa user from Jakub, #61149
- make cons.saver attr(4711, vcsa, root)
- require new dev package

* Thu Mar  7 2002 Havoc Pennington <hp@redhat.com>
- rebuild in new environment
- 4.5.55, with lots of patch-adapting to make it build

* Fri Jan 25 2002 Havoc Pennington <hp@redhat.com>
- rebuild in rawhide
- fix prefix/share -> datadir
- comment out gmc/mcserv subpackages, place order for asbestos suit

* Mon Aug 27 2001 Havoc Pennington <hp@redhat.com>
- Add po files from sources.redhat.com

* Sun Jul 22 2001 Havoc Pennington <hp@redhat.com>
- build requires gnome-libs-devel, #49518

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Apr 25 2001 Bill Nottingham <notting@redhat.com>
- fix mc-4.5.51-desktop.patch to work on ia64

* Mon Apr  2 2001 Preston Brown <pbrown@redhat.com>
- check return code of mount for failure (ewt)

* Thu Mar 22 2001 Owen Taylor <otaylor@redhat.com>
- Fix problem where CORBA notification wasn't working since last change.

* Fri Mar 16 2001 Owen Taylor <otaylor@redhat.com>
- Rescan devices on startup

* Mon Mar 12 2001  <jrb@redhat.com>
- remove man pages from mc.ext.in so that tgz and rpm browsing work in
  non LANG=C locales

* Wed Mar  7 2001 Owen Taylor <otaylor@redhat.com>
- Add patch to recognize kudzu's fstab entries
- Fix path to memstick icon

* Fri Feb 23 2001 Trond Eivind Glomsr鷣 <teg@redhat.com>
- use %%{_tmppath}
- langify

* Tue Feb 21 2001 Akira TAGOH <tagoh@redhat.com>
- Fixed install some desktop icons for specific language.

* Fri Feb 16 2001 Akira TAGOH <tagoh@redhat.com>
- Updated Red Hat JP desktop icons.

* Wed Feb 14 2001 Jakub Jelinek <jakub@redhat.com>
- include both sys/time.h and time.h on glibc 2.2.2
- fix Japanese patch to include locale.h.

* Tue Feb  6 2001 Trond Eivind Glomsr鷣 <teg@redhat.com>
- i18nize initscript

* Sat Jan 27 2001 Akira TAGOH <tagoh@redhat.com>
- Added Japanese patch(language specific desktop icons).

* Fri Jan 19 2001 Akira TAGOH <tagoh@redhat.com>
- Updated Japanese translation.

* Sun Jan 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not prereq %{_sysconfdir}/init.d
- do not require gpm for s390

* Mon Aug 21 2000 Jonathan Blandford <jrb@redhat.com>
- fixed bug 16467

* Thu Aug 17 2000 Tim Powers <timp@redhat.com>
- modified my patch (again) to free quoted

* Thu Aug 17 2000 Nalin Dahyabhai <nalin@redhat.com>
- run %%configure in the build phase, not the setup
- modify Tim's patch to always just edit one file

* Thu Aug 17 2000 Than Ngo <than@redhat.com>
- fix problems viewing the package (Bug #16378)

* Thu Aug 17 2000 Tim Powers <timp@redhat.com>
- fixed bug #16269

* Fri Aug  4 2000 Tim Waugh <twaugh@redhat.com>
- make stdout/stderr writable before forking

* Wed Aug 02 2000 Jonathan Blandford <jrb@redhat.com>
- Updated desktop entries.

* Thu Jul 20 2000 Bill Nottingham <notting@redhat.com>
- move initscript back

* Wed Jul 19 2000 Jonathan Blandford <jrb@redhat.com>
- make the togglebutton patch work correctly

* Tue Jul 18 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix syntax error in mcserv.init that crept in with condrestart

* Mon Jul 17 2000 Jonathan Blandford <jrb@redhat.com>
- added a toggle button to let people turn off the "you are running
  gmc as root" warning.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jul 10 2000 Preston Brown <pbrown@redhat.com>
- move initscript, add condrestart stuff

* Mon Jul 10 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- remove execute bits from config/pam files

* Mon Jul  3 2000 Jonathan Blandford
- Update to 4.5.51.  Now there is a trashcan!

* Thu Jun 15 2000 Owen Taylor <otaylor@redhat.com>
- Update to 4.5.49

* Fri Jun  2 2000 Nalin Dahyabhai <nalin@redhat.com>
- modify PAM setup to use system-auth

* Mon May 22 2000 Bill Nottingham <notting@redhat.com>
- hmmm, ia64 patches fell out.

* Fri May 19 2000 Jonathan Blandford <jrb@redhat.com>
- upgrade to new version of mc.
- removed builtincpio patch

* Tue Mar  7 2000 Jeff Johnson <jbj@redhat.com>
- rebuild for sparc baud rates > 38400.

* Wed Feb 22 2000 Preston Brown <pbrown@redhat.com>
- fix mc.sh, function was not exported

* Wed Feb 17 2000 Jakub Jelinek <jakub@redhat.com>
- builtin cpio vfs, change rpm extfs to use it -
  should speed up e.g. copyout from rpm by orders of magnitude
  patch by Jan Hudec <jhud7196@artax.karlin.mff.cuni.cz>
- fix buglet in the patch

* Mon Feb 14 2000 Preston Brown <pbrown@redhat.com>
- move redhat-logos depency to gmc (#9395)

* Fri Feb 4 2000 Jonathan Blandford <jrb@redhat.com>
- changed default rpm action to be upgrade.
- Changed locale to be in mc package, instead of gmc.

* Thu Feb 3 2000 Jonathan Blandford <jrb@redhat.com>
- use /bin/rm instead of rm so that aliases won't interfere with the
  script

* Fri Sep 25 1999 Bill Nottingham <notting@redhat.com>
- chkconfig --del in %preun, not %postun

* Wed Sep 22 1999 Michael Fulbright <drmike@redhat.com>
- updated to 4.5.39-pre9

* Wed Aug 04 1999 Michael K. Johnson <johnsonm@redhat.com>
- moved configure to setup
- buildrequires gpm-devel so mouse works in console

* Wed Jul 22 1999 Michael Fulbright <drmike@redhat.com>
- added ${prefix}/lib/mc/syntax to mc file list
- turned off samba support

* Wed Jul  7 1999 Jonathan Blandford <jrb@redhat.com>
- updated mc to work with mc 4.5.36.  Thanks to Brian Ryner
  <bryner@uiuc.edu> for providing the patch.

* Mon Apr 19 1999 Michael Fulbright <drmike@redhat.com>
- removed rpm menu defs - we depend on gnorpm for these
- fixed bug that caused crash if group doesnt exist for file

* Thu Apr 15 1999 Michael Fulbright <drmike@redhat.com>
- cleanup several dialogs

* Mon Apr 12 1999 Michael Fulbright <drmike@redhat.com>
- true version 4.5.30

* Fri Apr 09 1999 Michael Fulbright <drmike@redhat.com>
- version pre-4.5.30 with patch to make this link on alpha properly
  Mark as version 0.7 to denote not the official 4.5.30 release

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Wed Mar 31 1999 Michael Fulbright <drmike@redhat.com>
- fixed errata support URL

* Tue Mar 25 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.29
- added default desktop icons for Red Hat desktop
- added redhat-logos to requirements
- added README.desktop to doc list for gmc
- added locale data

* Fri Mar 25 1999 Preston Brown <pbrown@redhat.com>
- patched so that TERM variable set to xterm produces color

* Mon Mar 22 1999 Michael Fulbright <drmike@redhat.com>
- made sure %{_sysconfdir}/pam.d/mcserv has right permissions

* Thu Mar 18 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.27

* Tue Mar 16 1999 Michael Fulbright <drmike@redhat.com>
- fix'd icon display problem

* Sun Mar 14 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.25 AND 4.5.26

* Wed Mar 10 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.24

* Mon Feb 15 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.16
- removed mc.keys from mc file list

* Fri Feb 12 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.14
- fixed file list

* Sat Feb 06 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.11

* Wed Feb 03 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.10

* Fri Jan 22 1999 Michael Fulbright <drmike@redhat.com>
- added metadata to gmc file list

* Mon Jan 18 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.9

* Wed Jan 06 1999 Michael Fulbright <drmike@redhat.com>
- version 4.5.6

* Wed Dec 16 1998 Michael Fulbright <drmike@redhat.com>
- updated for GNOME freeze

* Thu Aug 20 1998 Michael Fulbright <msf@redhat.com>
- rebuilt against gnome-libs 0.27 and gtk+-1.1

* Thu Jul 09 1998 Michael Fulbright <msf@redhat.com>
- made cons.saver not setuid

* Sun Apr 19 1998 Marc Ewing <marc@redhat.com>
- removed tkmc

* Wed Apr 8 1998 Marc Ewing <marc@redhat.com>
- add %{prefix}/lib/mc/layout to gmc

* Tue Dec 23 1997 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>
- added --without-debug to configure,
- modification in %%build and %%install and cosmetic modification in packages
  headers,
- added %%{PACKAGE_VERSION} macro to Buildroot,
- removed "rm -rf $RPM_BUILD_ROOT" from prep section
- removed Packager field.

* Thu Dec 18 1997 Michele Marziani <marziani@fe.infn.it>
- Merged spec file with that from RedHat-5.0 distribution
  (now a Hurricane-based distribution is needed)
- Added patch for RPM script (didn't always work with rpm-2.4.10)
- Corrected patch for mcserv init file (chkconfig init levels)
- Added more documentation files on termcap, terminfo, xterm

* Thu Oct 30 1997 Michael K. Johnson <johnsonm@redhat.com>

- Added dependency on portmap

* Wed Oct 29 1997 Michael K. Johnson <johnsonm@redhat.com>

- fixed spec file.
- Updated to 4.1.8

* Sun Oct 26 1997 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>

- updated to 4.1.6
- added %attr macros in %%files,
- a few simplification in %%install,
- removed glibc patch,
- fixed installing %{_sysconfdir}/X11/wmconfig/tkmc.

* Thu Oct 23 1997 Michael K. Johnson <johnsonm@redhat.com>

- updated to 4.1.5
- added wmconfig

* Wed Oct 15 1997 Erik Troan <ewt@redhat.com>

- chkconfig is for mcserv package, not mc one

* Tue Oct 14 1997 Erik Troan <ewt@redhat.com>

- patched init script for chkconfig
- don't turn on the service by default

* Fri Oct 10 1997 Michael K. Johnson <johnsonm@redhat.com>

- Converted to new PAM conventions.
- Updated to 4.1.3
- No longer needs glibc patch.

* Thu May 22 1997 Michele Marziani <marziani@fe.infn.it>

- added support for mc alias in %{_sysconfdir}/profile.d/mc.csh (for csh and tcsh)
- lowered number of SysV init scripts in %{_sysconfdir}/rc.d/rc[0,1,6].d
  (mcserv needs to be killed before inet)
- removed all references to $RPM_SOURCE_DIR
- restored $RPM_OPT_FLAGS when compiling
- minor cleanup of spec file: redundant directives and comments removed

* Sun May 18 1997 Michele Marziani <marziani@fe.infn.it>

- removed all references to non-existent mc.rpmfs
- added mcedit.1 to the %files section
- reverted to un-gzipped man pages (RedHat style)
- removed double install line for mcserv.pamd

* Tue May 13 1997 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>

- added new rpmfs script,
- removed mcfn_install from mc (adding mc() to bash enviroment is in
  %{_sysconfdir}/profile.d/mc.sh),
- %{_sysconfdir}/profile.d/mc.sh changed to %config,
- removed %{prefix}/lib/mc/bin/create_vcs,
- removed %{prefix}/lib/mc/term.

* Wed May 9 1997 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>

- changed source url,
- fixed link mcedit to mc,

* Tue May 7 1997 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>

- new version 3.5.27,
- %dir %{prefix}/lib/mc/icons and icons removed from tkmc,
- added commented xmc part.

* Tue Apr 22 1997 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>

- FIX spec:
   - added URL field,
   - in mc added missing %{prefix}/lib/mc/mc.ext, %{prefix}/lib/mc/mc.hint,
     %{prefix}/lib/mc/mc.hlp, %{prefix}/lib/mc/mc.lib, %{prefix}/lib/mc/mc.menu.

* Fri Apr 18 1997 Tomasz K這czko <kloczek@rudy.mif.pg.gda.pl>

- added making packages: tkmc, mcserv (xmc not work yet),
- gziped man pages,
- added %{_sysconfdir}/pamd.d/mcserv PAM config file.
- added instaling icons,
- added %{_sysconfdir}/profile.d/mc.sh,
- in %doc added NEWS README,
- removed %{prefix}/lib/mc/FAQ,
- added mcserv.init script for mcserv (start/stop on level 86).
