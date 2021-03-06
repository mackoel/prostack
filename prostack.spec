%global __jar_repack %{nil}
%global prostackserverhome /var/www/prostack

Name:           prostack
Version:        7.0.10
Release:        0%{?dist}
Summary:        ProStack common part

Group:          Graphics
License:        GPLv3
URL:            http://prostack.sourceforge.net/
Source0:        http://sourceforge.net/projects/prostack/files/%{name}-%{version}.tgz
#BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}

BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: lua
BuildRequires: texlive-tex4ht
BuildRequires: goocanvas-devel
BuildRequires: liberation-mono-fonts
BuildRequires: gtk2-devel
BuildRequires: gtk3-devel
BuildRequires: glib2-devel
BuildRequires: libtiff-devel
BuildRequires: gnutls-devel
BuildRequires: libsoup-devel
BuildRequires: sqlite-devel
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: httpd-devel
BuildRequires: gsl-devel
BuildRequires: gts-devel
BuildRequires: fftw-devel
BuildRequires: atlas
BuildRequires: libtool
BuildRequires: intltool
BuildRequires: perl-XML-Parser
BuildRequires: pkgconfig
BuildRequires: texlive-collection-latex
BuildRequires: texlive-preview
BuildRequires: texlive-collection-latexextra
BuildRequires: texlive-collection-latexrecommended
BuildRequires: texlive-collection-htmlxml
BuildRequires: texlive-collection-langenglish
BuildRequires: texlive-collection-langeuropean
BuildRequires: texlive-collection-pictures
BuildRequires: texlive-ifsym
BuildRequires: texlive-latex-fonts
BuildRequires: texlive-ltxtools
BuildRequires: ImageMagick

Requires: glib2
Requires: libtiff
Requires: gnutls
Requires: libsoup
Requires: sqlite
Requires: apr
Requires: apr-util
Requires: httpd
Requires: gnuplot
Requires: ImageMagick
Requires: curl
Requires: gsl
Requires: gts
Requires: fftw
Requires: R

%description
ProStack is the Image Processing Platform that allows to build complex scenarios

%package devel
Summary:        ProStack headers
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}

%description devel
includes for image processing workflows

%package server
Summary:        ProStack server
Group:          System Environment/Daemons
Requires:       %{name} = %{version}-%{release}

%description server
Apache2 module to run ProStack image rocessing workflows

%package desktop
Summary:        ProStack desktop
Group:          Graphics
Requires:       %{name} = %{version}-%{release}

Obsoletes:      prostack-main

%description desktop
GTK+3.0 GUI to run ProStack image processing workflows

%package doc
Summary:        ProStack documentation
Group:          Graphics
Requires:       %{name} = %{version}-%{release}

%description doc
Documentation for ProStack

%package examples
Summary:        ProStack examples
Group:          Graphics
Requires:       %{name} = %{version}-%{release}

%description examples
Example workflows for ProStack

%package omero
Summary:        ProStack support for OMERO
Group:          Graphics
Requires:       %{name} = %{version}-%{release}

%description omero
ProStack is the Image Processing Platform that allows to build complex scenarios. This package adds support for OMERO.
This package adds a browser for OMERO repository to be used in ProStack scenario builder.

%package rascon
Summary:        ProStack support for rasdaman
Group:          Graphics
Requires:       %{name} = %{version}-%{release} rasdaman >= 8.0.0

%description rascon
ProStack is the Image Processing Platform that allows to build complex scenarios. This package adds support for rasdaman.

%prep
%setup -q

%build

%install
rm -rf %{buildroot}

d=`pwd`

for f in door prostak quastack glaz prostack iapee cmove prutik rascon frameproc
do
	cd $f
	autoreconf -fi
	./configure --prefix=/usr --docdir=%{_docdir}/$f --libdir=%{_libdir}
	make DESTDIR=%{buildroot}
	make install DESTDIR=%{buildroot}
	cd $d
done

# install server
cd mod_prostack
./autogen.sh --prefix=/usr --docdir=%{_docdir}/mod_prostack --libdir=%{_libdir}/httpd/modules --sysconfdir=%{_sysconfdir}
make DESTDIR=%{buildroot}
make install DESTDIR=%{buildroot}
cd $d

# install doc
mkdir -p %{buildroot}%{_datadir}/prostack/html
cd Documentation
htlatex ProStackUserGuide4.tex "html,2,frames" "" "-d%{buildroot}%{_datadir}/prostack/html/" ""
cd $d

# install examples
cd examples
autoreconf -f -i
./configure --prefix=/usr --docdir=%{_docdir}/examples
make
make install DESTDIR=%{buildroot}
cd $d

# install omero
cd omep
autoreconf -f -i
mkdir build
./configure --prefix=/usr --docdir=%{_docdir}/omep --libdir=%{_libdir}
make DESTDIR=%{buildroot}
cat Makefile | sed -e "s/ src //g" > Makefile.1
make -f Makefile.1 install DESTDIR=%{buildroot}
mkdir -p %{buildroot}/usr/share/prostack/java
cp -R build %{buildroot}/usr/share/prostack/java
cd $d

rm -f %{buildroot}/usr/share/mime/XMLnamespaces
rm -f %{buildroot}/usr/share/mime/aliases
rm -f %{buildroot}/usr/share/mime/application/x-prostack.xml
rm -f %{buildroot}/usr/share/mime/generic-icons
rm -f %{buildroot}/usr/share/mime/globs
rm -f %{buildroot}/usr/share/mime/globs2
rm -f %{buildroot}/usr/share/mime/icons
rm -f %{buildroot}/usr/share/mime/magic
rm -f %{buildroot}/usr/share/mime/mime.cache
rm -f %{buildroot}/usr/share/mime/subclasses
rm -f %{buildroot}/usr/share/mime/treemagic
rm -f %{buildroot}/usr/share/mime/types
rm -f %{buildroot}/usr/share/mime/version

%find_lang door
%find_lang iapee
%find_lang prostack
%find_lang glaz
%find_lang prutik

cat iapee.lang prostack.lang glaz.lang prutik.lang > desktop.lang

# Create home for our user
install -d -m 700 %{buildroot}%{prostackserverhome}

%clean
rm -rf %{buildroot}

%post desktop
/sbin/ldconfig
if which update-mime-database>/dev/null 2>&1; then \
	update-mime-database %{_datadir}/mime; \
fi
if [ -d %{_datadir}/imagej/macros ]; then \
    cp %{_datadir}/prostack/fiji/ProStackMacro*.txt %{_datadir}/imagej/macros; \
fi
if [ -e %{_datadir}/door/kimono-db.db.en_US.UTF-8 ]; then \
	cat %{_datadir}/door/prutik-db.en_US.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.en_US.UTF-8; \
	cat %{_datadir}/door/glaz-db.en_US.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.en_US.UTF-8; \
	cat %{_datadir}/door/iapee-db.en_US.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.en_US.UTF-8; \
fi
if [ -e %{_datadir}/door/kimono-db.db.ru_RU.UTF-8 ]; then \
	cat %{_datadir}/door/prutik-db.ru_RU.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.ru_RU.UTF-8; \
	cat %{_datadir}/door/glaz-db.ru_RU.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.ru_RU.UTF-8; \
	cat %{_datadir}/door/iapee-db.ru_RU.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.ru_RU.UTF-8; \
fi

%postun desktop
/sbin/ldconfig
if which update-mime-database>/dev/null 2>&1; then \
	update-mime-database %{_datadir}/mime; \
fi
if [ $1 -eq 0 ]; then \
	if [ -d %{_datadir}/imagej/macros ]; then \
		rm -f %{_datadir}/imagej/macros/ProStackMacro*.txt; \
	fi; \
fi

%post omero
if [ -e %{_datadir}/door/kimono-db.db.en_US.UTF-8 ]; then \
	cat %{_datadir}/door/omep-db.en_US.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.en_US.UTF-8; \
fi
if [ -e %{_datadir}/door/kimono-db.db.ru_RU.UTF-8 ]; then \
	cat %{_datadir}/door/omep-db.ru_RU.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.ru_RU.UTF-8; \
fi

%post rascon
if [ -e %{_datadir}/door/kimono-db.db.en_US.UTF-8 ]; then \
	cat %{_datadir}/door/rascon-db.en_US.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.en_US.UTF-8; \
fi
if [ -e %{_datadir}/door/kimono-db.db.ru_RU.UTF-8 ]; then \
	cat %{_datadir}/door/rascon-db.ru_RU.UTF-8.sqlt3 | sqlite3 %{_datadir}/door/kimono-db.db.ru_RU.UTF-8; \
fi

%files -f door.lang
%defattr(-,root,root,-)
%{_bindir}/apro.pl
%{_bindir}/apron.pl
%{_bindir}/archplot.pl
%{_bindir}/cmove
%{_bindir}/komet
%{_bindir}/door_copy
%{_bindir}/door_convert_type
%{_bindir}/nplot.pl
%{_bindir}/nplot2.pl
%{_bindir}/nplot3.pl
%{_bindir}/prostak
%{_bindir}/frame_proc_cell_rm
%{_bindir}/frame_proc_clust
%{_bindir}/frame_proc_filt
%{_bindir}/frame_proc_xcells
%{_bindir}/series_proc_summary
%{_bindir}/frame_proc_cells
%{_bindir}/frame_proc_clust_k
%{_bindir}/frame_proc_obj
%{_bindir}/frame_proc_polarplot
%{_bindir}/series_proc_xsummary
%doc %{_docdir}/cmove
%doc %{_docdir}/door
%doc %{_docdir}/prostak
%doc %{_docdir}/quastack
%doc %{_docdir}/frameproc
%{_libdir}/libdoor.so
%{_libdir}/libdoor.so.*
%{_libdir}/libgrf.so
%{_libdir}/libgrf.so.*
%{_libdir}/libparus.so
%{_libdir}/libparus.so.*
%{_datadir}/door/kimono-*
%{_datadir}/door/cmove-*
%{_datadir}/door/prostak-*
%{_datadir}/door/quastak-*
%{_datadir}/door/frameproc-*

%files desktop -f desktop.lang
%defattr(-,root,root,-)
%{_bindir}/prostack-bambu
%{_bindir}/prostack-execute
%{_bindir}/glaz
%{_bindir}/iapee
%{_bindir}/prostack
%{_bindir}/prutik
%doc %{_docdir}/glaz
%doc %{_docdir}/iapee
%doc %{_docdir}/prostack
%doc %{_docdir}/prutik
%{_datadir}/applications/prostack.desktop
%{_datadir}/dbus-1/services/ru.spbstu.sysbio.ProStack.service
%{_datadir}/glaz
%{_datadir}/iapee
%dir %{_datadir}/icons/gnome/48x48/mimetypes/
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-prostack.png
%{_datadir}/prostack
%{_datadir}/mime/packages/prostack.xml
%{_datadir}/pixmaps/prostack_icon.png
%{_datadir}/prostack/fiji
%{_datadir}/prutik
%{_datadir}/door/prutik-*
%{_datadir}/door/glaz-*
%{_datadir}/door/iapee-*

%files server
%defattr(-,root,root,-)
%{_docdir}/mod_prostack
%{_libdir}/httpd/modules/mod_prostack.so
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd/conf.d/prostack.conf
%attr(700,apache,apache) %dir %{prostackserverhome}

%files doc
%defattr(-,root,root,-)
%dir %{_datadir}/prostack/html
%{_datadir}/prostack/html/ProStackUserGuide4*

%files examples
%defattr(-,root,root,-)
%{_datadir}/prostack/examples

%files omero
%defattr(-,root,root,-)
%{_datadir}/prostack/java/libs/
%{_datadir}/prostack/java/build/ome/prostack/Main.class
%{_datadir}/prostack/java/build/ome/prostack/OmeroProStack.class
%{_datadir}/prostack/java/build/ome/prostack/data/DSAccessException.class
%{_datadir}/prostack/java/build/ome/prostack/data/DSOutOfServiceException.class
%{_datadir}/prostack/java/build/ome/prostack/data/DataService.class
%{_datadir}/prostack/java/build/ome/prostack/data/DataServiceImpl.class
%{_datadir}/prostack/java/build/ome/prostack/data/Gateway.class
%{_datadir}/prostack/java/build/ome/prostack/data/ImageObject.class
%{_datadir}/prostack/java/build/ome/prostack/data/KeepClientAlive.class
%{_datadir}/prostack/java/build/ome/prostack/data/PojoMapper.class
%{_datadir}/prostack/java/build/ome/prostack/data/ServicesFactory.class
%{_datadir}/prostack/java/build/ome/prostack/dm/actions/*.class
%{_datadir}/prostack/java/build/ome/prostack/dm/browser/*.class
%{_datadir}/prostack/java/build/ome/prostack/dm/util/*.class
%{_datadir}/prostack/java/build/ome/prostack/dm/*.class
%{_datadir}/prostack/java/build/ome/prostack/OmeroBrowser.class
%doc %{_docdir}/omep/*
%{_datadir}/door/omep-*

%files rascon
%defattr(-,root,root,-)
%{_bindir}/lazyrasql
%doc %{_docdir}/rascon
%{_datadir}/door/rascon-*

%files devel
%defattr(-,root,root,-)
%{_includedir}/libdoor
%{_includedir}/libgrf
%{_includedir}/libparus
%{_libdir}/pkgconfig/libdoor-1.0.pc
%{_libdir}/libgrf.a
%{_libdir}/libgrf.la
%{_libdir}/libparus.a
%{_libdir}/libparus.la
%{_libdir}/libdoor.a
%{_libdir}/libdoor.la

%changelog

* Wed Jul 26  2017 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.10

- Fix deps for F25-26 and removed psocv

* Tue May 17  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.10

- New version

* Fri Apr 29  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.8

- New version

* Thu Mar 10  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.7

- New version

* Sat Feb 20  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.6

- New version

* Wed Feb 17  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.5

- New version

* Tue Feb 09  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.4

- New version

* Tue Feb 02  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.3

- New version

* Fri Jan 29  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.2

- New version

* Fri Jan 22  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.1

- New version

* Thu Jan 21  2016 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 7.0.0

- New version

* Mon Dec 21  2015 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 6.5.3

- New version

* Thu Dec 17  2015 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 6.5.2

- New version

* Mon Dec 14  2015 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 6.5.1

- New version

* Tue Dec 01  2015 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 6.5.0

- New version

* Wed Sep 09  2015 Konstantin Kozlov <kozlov_kn@spbstu.ru> - 6.3.0

- New version

* Wed Feb 08  2012 Konstantin Kozlov <kkozlov@prostack.ru> - 3.0.0

- Rascon got lazyrasql
- door got door_convert_type

* Wed Feb 01  2012 Konstantin Kozlov <kkozlov@prostack.ru> - 3.0.0

- Updated sources and requirements

