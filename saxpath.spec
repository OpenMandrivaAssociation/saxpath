Name:       saxpath
Version:    1.0
Release:    2.7
Summary:    Simple API for XPath

Group:      Development/Java
License:    Saxpath
URL:        http://sourceforge.net/projects/saxpath/
Source0:    http://downloads.sourceforge.net/saxpath/saxpath-1.0.tar.gz
Source1:    %{name}-%{version}.pom
BuildRoot:  %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:  ant
BuildRequires:  ant-junit
BuildRequires:  ant-trax
BuildRequires: java-rpmbuild
Requires:       jpackage-utils

BuildArch:      noarch

%description
The SAXPath project is a Simple API for XPath. SAXPath is analogous to SAX
in that the API abstracts away the details of parsing and provides a simple
event based callback interface.

%package javadoc
Summary:    Javadoc for saxpath
Group:      Development/Java
Requires:   jpackage-utils

%description javadoc
Java API documentation for saxpath.

%prep
%setup -q -n %{name}-%{version}-FCS

find -type f -name "*.jar" -exec rm -f '{}' \;

%build
mkdir src/conf
touch src/conf/MANIFEST.MF

export CLASSPATH=$(build-classpath xalan-j2-serializer)

ant

# fix rpmlint warings: saxpath-javadoc.noarch: W: wrong-file-end-of-line-encoding /usr/share/javadoc/saxpath/**/*.css
for file in `find build/doc -type f | grep .css`; do
    %{__sed} -i 's/\r//g' $file
done

%install
rm -rf $RPM_BUILD_ROOT

# install jar
install -dm 755 $RPM_BUILD_ROOT/%{_javadir}
cp -p build/saxpath.jar $RPM_BUILD_ROOT/%{_javadir}/%{name}-%{version}.jar
ln -s %{name}-%{version}.jar $RPM_BUILD_ROOT/%{_javadir}/%{name}.jar

#install pom
install -dm 755 $RPM_BUILD_ROOT/%{_datadir}/maven2/poms
cp -p %{SOURCE1} $RPM_BUILD_ROOT/%{_datadir}/maven2/poms/JPP-saxpath.pom

#depmap entry
%add_to_maven_depmap saxpath saxpath %{version}-FCS JPP saxpath

# install javadoc
install -dm 755 $RPM_BUILD_ROOT/%{_javadocdir}/%{name}
cp -a build/doc/* $RPM_BUILD_ROOT/%{_javadocdir}/%{name}/

%post
%update_maven_depmap

%postun
%update_maven_depmap

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_javadir}/*
%{_datadir}/maven2/poms/*
%{_mavendepmapfragdir}

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/*


