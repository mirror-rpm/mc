Summary:	User-friendly text console file manager and visual shell.
Name:		mc
Version:	4.6.1a
Release:	0.4
Epoch:		1
License:	GPL
Group:		System Environment/Shells
#Source0:	http://www.ibiblio.org/pub/Linux/utils/file/managers/mc/mc-%{version}.tar.gz
%define date 20050202
Source0:	mc-%{version}-%{date}.tar.bz2
URL:		http://www.ibiblio.org/mc/
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
BuildRequires:	gpm-devel, slang-devel, glib2-devel
BuildRequires:	XFree86-devel, e2fsprogs-devel, gettext, gettext-devel
Requires:	dev >= 0:3.3-3

Patch0:		mc-utf8.patch
Patch1:		mc-extensions.patch
Patch2:		mc-promptfix.patch
Patch3:		mc-uglydir.patch
Patch4:		mc-fish-upload.patch

%description
Midnight Commander is a visual shell much like a file manager, only
with many more features. It is a text mode application, but it also
includes mouse support if you are running GPM. Midnight Commander's
best features are its ability to FTP, view tar and zip files, and to
poke into RPMs for specific files.

%prep
%setup -q -n mc-%{version}-%{date}

%patch0 -p1 -b .utf8
%patch1 -p1 -b .extensions
%patch2 -p1 -b .promptfix
%patch3 -p1 -b .uglydir
%patch4 -p1 -b .fish-upload

# convert files in /lib to UTF-8
pushd lib
for i in mc.hint mc.hint.es mc.hint.it mc.hint.nl; do
  iconv -f iso-8859-1 -t utf-8 < ${i} > ${i}.tmp
  mv -f ${i}.tmp ${i}
done

for i in mc.hint.cs mc.hint.hu mc.hint.pl; do
  iconv -f iso-8859-2 -t utf-8 < ${i} > ${i}.tmp
  mv -f ${i}.tmp ${i}
done

for i in mc.hint.sr mc.menu.sr; do
  iconv -f iso-8859-5 -t utf-8 < ${i} > ${i}.tmp
  mv -f ${i}.tmp ${i}
done

iconv -f koi8-r -t utf8 < mc.hint.ru > mc.hint.ru.tmp
mv -f mc.hint.ru.tmp mc.hint.ru
iconv -f koi8-u -t utf8 < mc.hint.uk > mc.hint.uk.tmp
mv -f mc.hint.uk.tmp mc.hint.uk
iconv -f big5 -t utf8 < mc.hint.zh > mc.hint.zh.tmp
mv -f mc.hint.zh.tmp mc.hint.zh
popd


# convert man pages in /doc to UTF-8
pushd doc

pushd ru
for i in mc.1.in xnc.hlp; do
  iconv -f koi8-r -t utf-8 < ${i} > ${i}.tmp
  mv -f ${i}.tmp ${i}
done
popd

pushd sr
for i in mc.1.in mcserv.8.in xnc.hlp; do
  iconv -f iso-8859-5 -t utf-8 < ${i} > ${i}.tmp
  mv -f ${i}.tmp ${i}
done
popd

for d in es it; do
  for i in mc.1.in xnc.hlp; do
    iconv -f iso-8859-3 -t utf-8 < ${d}/${i} > ${d}/${i}.tmp
    mv -f ${d}/${i}.tmp ${d}/${i}
  done
done

for d in hu pl; do
  for i in mc.1.in xnc.hlp; do
    iconv -f iso-8859-2 -t utf-8 < ${d}/${i} > ${d}/${i}.tmp
    mv -f ${d}/${i}.tmp ${d}/${i}
  done
done

popd

%build
export CFLAGS="-D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE $RPM_OPT_FLAGS"
%configure --with-screen=slang \
	     --host=%{_host} --build=%{_build} \
	     --target=%{_target_platform} \
	     --program-prefix=%{?_program_prefix} \
	     --prefix=%{_prefix} \
	     --exec-prefix=%{_exec_prefix} \
	     --bindir=%{_bindir} \
	     --sbindir=%{_sbindir} \
	     --sysconfdir=%{_sysconfdir} \
	     --datadir=%{_datadir} \
	     --includedir=%{_includedir} \
	     --libdir=%{_libdir} \
	     --libexecdir=%{_libexecdir} \
	     --localstatedir=%{_localstatedir} \
	     --sharedstatedir=%{_sharedstatedir} \
	     --mandir=%{_mandir} \
	     --infodir=%{_infodir} \
	     --enable-charset
make %{?_smp_mflags}

%install 
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

%{makeinstall} sysconfdir=$RPM_BUILD_ROOT%{_sysconfdir}

install lib/{mc.sh,mc.csh} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d

# install charsets, bug #76486
install -m 644 lib/mc.charsets $RPM_BUILD_ROOT%{_datadir}/mc

# install man pages in various languages
for l in es hu it pl ru sr; do
mkdir -p $RPM_BUILD_ROOT%{_mandir}/${l}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/${l}/man1
gzip -nf9 doc/${l}/mc.1
install -m 644 doc/${l}/mc.1.gz $RPM_BUILD_ROOT%{_mandir}/${l}/man1
done

for I in /etc/pam.d/mcserv \
	/etc/rc.d/init.d/mcserv \
	/etc/mc.global; do
	rm -rf ${RPM_BUILD_ROOT}${I}
done

%find_lang %{name}

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
%lang(es) %{_mandir}/es/man1/mc.1.gz
%lang(hu) %{_mandir}/hu/man1/mc.1.gz
%lang(it) %{_mandir}/it/man1/mc.1.gz
%lang(pl) %{_mandir}/pl/man1/mc.1.gz
%lang(ru) %{_mandir}/ru/man1/mc.1.gz
%lang(sr) %{_mandir}/sr/man1/mc.1.gz
%config %{_sysconfdir}/profile.d/*
%dir %{_libdir}/mc
%dir %{_datadir}/mc

%changelog
* Wed Feb  2 2005 Jindrich Novy <jnovy@redhat.com> 4.6.1a-0.4
- update from CVS (fixes #143586)
- merge all UTF-8 related patches to single .utf8 patch
- drop BuildRequires gettext-devel, autopoint no more needed

* Tue Dec 21 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1a-0.3
- rewrote mbstrlen() in utf8 patch, this fixes:
  - dir name truncation in command prompt for ja_JP, ko_KR locales (#142706)
  - localized texts will fit dialog windows and pull-down menus - tweak create_menu()
  - dialog titles are centered correctly
- fix bad displaying of mc logo in help (#143415)
- merge msglen patch with utf8 patch

* Wed Dec 15 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1a-0.2
- update from CVS - problem in uzip.in fixed by upstream (#141844)
- fix msglen patch to deal with wide UTF-8 characters (#141875)

* Wed Dec  9 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1a-0.1
- update from CVS
- sync UTF-8 patches with upstream
- drop upstreamed badsize, growbuf patches
- faster FISH upload support (#140750) - from Dmitry Butskoj

* Mon Dec  6 2004 Jindrich Novy <jnovy@redhat.com>
- add msglen patch to calculate message length correctly in UTF-8 (#141875)
  (thanks to Nickolay V. Shmyrev)
- convert hints for ru, uk, zh, man page conversion fix

* Wed Dec  1 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.11
- update from CVS
  - fix #141095 - extraction of symlinks from tarfs is now fine
- add growbuf patch from Roland Illig #141422 to view files
  in /proc and /sys properly

* Fri Nov 24 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.10
- update from CVS
- update promptfix patch, drop upstreamed strippwd patch
- add badsize patch to fix displaying of filesizes >2GB
- sync UTF-8 patches with upstream
- replace autogen.sh style with configure

* Fri Nov 12 2004 Jindrich Novy <jnovy@redhat.com>
- convert man pages to UTF-8 (#138871)

* Thu Nov  8 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.9
- update from CVS
- convert help files in /doc to UTF-8
- add --enable-charset (#76486)
- drop upstreamed 8bitdefault, extfs patch
- update partially upstreamed strippwd and extension patches
- add UTF-8 help patch from Vladimir Nadvornik (#136826)
- add promptfix patch

* Wed Nov  3 2004 Jindrich Novy <jnovy@redhat.com>
- drop upstreamed smallpatches patch
- install non-en man pages and fix encoding (#137036)
- fix possible mem leak in strippwd patch

* Fri Oct 22 2004 Jindrich Novy <jnovy@redhat.com>
- drop second part of the uglydir patch to display panel title
  correctly in UTF8 (#136129)

* Wed Oct 20 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.8
- update from CVS
- drop mc-php.syntax, more recent version in upstream
- add utf8-input patch
- sync strippwd, uglydir, extensions patches with upstream
- add 8bitdefault patch to enable 8-bit input by default

* Fri Oct 15 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.7
- update from CVS
- sync strippwd patch with upstream
- merged hp48.in patch to extfs patch (from Leonard den Ottolander)
- rebuilt

* Thu Oct 08 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.6
- update from CVS
- drop upstreamed vcsa and xtermaliases patches
- sync the rest of the patches with upstream
- update strippwd patch to eliminate passwords from dir hotlist
  and chdir error messages
- update perl scripts (Leonard den Ottolander, #127973, CAN-2004-0494)

* Wed Sep 22 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.5
- fixed password elimination when no '/' is present in URL

* Tue Sep 21 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.4
- fixed .strippwd patch to deal better with ':' and '@' in URL

* Thu Sep 17 2004 Jindrich Novy <jnovy@redhat.com> 4.6.1-0.3
- patch to prevent displaying passwords in ftp paths (#131088)
  - also removes pswd from Delete/Copy/Error dialogs, etc.
- added patch to fix/add extensions in mc.ext.in (#124242)

* Thu Sep 17 2004 Karel Zak <zakkr@zf.jcu.cz>
- patch to prevent hangs on directory with '\n' in name, (#127164)
- UTF8 hints support
- original hint files conversion to UTF8 in the spec file

* Mon Sep  6 2004 Jakub Jelinek <jakub@redhat.com> 4.6.1-0.2
- update from CVS
- remove absoluterm and troff patches

* Thu Sep  2 2004 Jakub Jelinek <jakub@redhat.com> 4.6.1-0.1
- update from CVS
  - handle INFO/LICENSE and INFO/OBSOLETES in rpm vfs (#67341)
- remove mc-cvs-unzip (#85073)
- fix hotkey handling when not UTF-8 (Leonard den Ottolander, #120735)
- allow terminal aliases for keys in mc.lib and ~/mc/ini,
  add gnome, xterm-new and rxvt aliases for xterm (#128163)

* Sat Aug 21 2004 Jakub Jelinek <jakub@redhat.com> 4.6.0-18
- 3 more quoting omissions in a.in

* Sat Aug 21 2004 Jakub Jelinek <jakub@redhat.com> 4.6.0-17
- fix shell quoting in extfs perl scripts
  (Leonard den Ottolander, #127973, CAN-2004-0494)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Apr 16 2004 Jakub Jelinek <jakub@redhat.com> 4.6.0-15
- don't use mmap if st_size doesn't fit into size_t
- fix one missed match_normal -> match_regex

* Fri Apr 16 2004 Jakub Jelinek <jakub@redhat.com> 4.6.0-14
- avoid buffer overflows in mcedit Replace function

* Wed Apr 14 2004 Jakub Jelinek <jakub@redhat.com> 4.6.0-13
- perl scripting fix

* Wed Apr 14 2004 Jakub Jelinek <jakub@redhat.com> 4.6.0-12
- fix a bug in complete.c introduced by last patch
- export MC_TMPDIR env variable
- avoid integer overflows in free diskspace % counting
- put temporary files into $MC_TMPDIR tree if possible,
  use mktemp/mkdtemp

* Mon Apr  5 2004 Jakub Jelinek <jakub@redhat.com> 4.6.0-11
- fix a bunch of buffer overflows and memory leaks (CAN-2004-0226)
- fix hardlink handling in cpio filesystem
- fix handling of filenames with single/double quotes and backslashes
  in %{_datadir}/mc/extfs/rpm
- update php.syntax file (#112645)
- fix crash with large syntax file (#112644)
- update CAN-2003-1023 fix to still make vfs symlinks relative,
  but with bounds checking

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Jan 17 2004 Warren Togami <wtogami@redhat.com> 4.6.0-9
- rebuild

* Sat Jan 17 2004 Warren Togami <wtogami@redhat.com> 4.6.0-7
- BuildRequires glib2-devel, slang-devel, XFree86-devel,
  e2fsprogs-devel, gettext
- Copyright -> License
- PreReq -> Requires
- Explicit zero epoch in versioned dev dep
- /usr/share/mc directory ownership
- Improve summary
- (Seth Vidal QA) fix for CAN-2003-1023 (Security)

* Tue Oct 28 2003 Jakub Jelinek <jakub@redhat.com> 4.6.0-6
- rebuilt to get correct PT_GNU_STACK setting

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

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
