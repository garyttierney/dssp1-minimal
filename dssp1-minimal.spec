%global commit0 ...
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 ...
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

%define POLICYVER 30
%define POLICYCOREUTILSVER 2.5

Summary: Defensec SELinux Security Policy
Name: dssp1
Version: 1.0
Release: %(date +%Y%%m%%d)git%{shortcommit0}%{?dist}
License: Public Domain
Group: System Environment/Base
Source0: https://github.com/Defensec/dssp1-minimal/archive/%{commit0}/dssp1-minimal-%{commit0}.tar.gz
Source1: https://github.com/Defensec/dssp1-base/archive/%{commit1}/dssp1-base-%{commit1}.tar.gz
URL: https://github.com/Defensec/dssp1-minimal/wiki
Requires: policycoreutils >= %{POLICYCOREUTILSVER}
Conflicts: selinux-policy
BuildRequires: policycoreutils >= %{POLICYCOREUTILSVER}
BuildArch: noarch

%description
SELinux security policy with a strong focus on flexibility and accessibility.
Provides the Defensec SELinux Security Policy base package.

%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%dir %{_sysconfdir}/selinux
%ghost %config(noreplace) %{_sysconfdir}/selinux/config
%ghost %{_sysconfdir}/sysconfig/selinux

%define fileList() \
%defattr(-,root,root,-) \
%dir %{_sysconfdir}/selinux/%1 \
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/seusers \
%dir %{_sysconfdir}/selinux/%1/logins \
%dir %{_sharedstatedir}/selinux/%1/active \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/semanage.read.LOCK \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/semanage.trans.LOCK \
%dir %attr(700,root,root) %dir %{_sharedstatedir}/selinux/%1/active/modules \
%verify(not md5 size mtime) %{_sharedstatedir}/selinux/%1/active/modules/100 \
%dir %{_sysconfdir}/selinux/%1/policy/ \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/policy/policy.%{POLICYVER} \
%dir %{_sysconfdir}/selinux/%1/contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/customizable_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/securetty_types \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/dbus_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/openssh_contexts \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/default_type \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/failsafe_context \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/removable_context \
%dir %{_sysconfdir}/selinux/%1/contexts/files \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/media \
%config(noreplace) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.subs_dist \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.bin \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs \
%verify(not md5 size mtime) %{_sysconfdir}/selinux/%1/contexts/files/file_contexts.homedirs.bin \
%{_sharedstatedir}/selinux/%1/active/commit_num \
%{_sharedstatedir}/selinux/%1/active/users_extra \
%{_sharedstatedir}/selinux/%1/active/homedir_template \
%{_sharedstatedir}/selinux/%1/active/seusers \
%{_sharedstatedir}/selinux/%1/active/file_contexts \
%{_sharedstatedir}/selinux/%1/active/policy.kern \
%dir %{_sysconfdir}/selinux/%1/contexts/users \
%nil

%package minimal
Summary: Minimal Defensec SELinux Security Policy
Group: System Environment/Base
Requires(pre): policycoreutils >= %{POLICYCOREUTILSVER}
Requires(pre): dssp1 = %{version}-%{release}
Requires: dssp1 = %{version}-%{release}

%description minimal
SELinux security policy with a strong focus on flexibility and accessibility.
Provides the minimal Defensec SELinux Security Policy package.

%files minimal
%fileList dssp1-minimal

%prep
%autosetup -n dssp1-minimal-%{commit0}
%autosetup -n dssp1-minimal-%{commit0} -a 1
rmdir src/base
mv -f dssp1-base-%{commit1} src/base

%build

%install
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/logins
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts
install -m0644 config/customizable_types %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/customizable_types
install -m0644 config/securetty_types %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/securetty_types
install -m0644 config/dbus_contexts %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/dbus_contexts
install -m0644 config/default_contexts %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/default_contexts
install -m0644 config/default_type %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/default_type
install -m0644 config/failsafe_context %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/failsafe_context
install -m0644 config/openssh_contexts %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/openssh_contexts
install -m0644 config/removable_context %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/removable_context
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/files
install -m0644 config/media %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/files/media
install -m0644 config/file_contexts.subs_dist %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/files/file_contexts.subs_dist
%{__mkdir} -p %{buildroot}%{_sysconfdir}/selinux/dssp1-minimal/contexts/users
%{__mkdir} -p %{buildroot}%{_sharedstatedir}/selinux
semodule -p %{buildroot} --priority=100 \
	-i `/bin/find ./src -type f \( -iname "*.cil" \) | /bin/cut -d/ -f2-` \
	-N -s dssp1-minimal

%clean
rm -rf %{buildroot}

%post minimal
if [ ! -s /etc/selinux/config ]; then
echo "
SELINUX=enforcing
SELINUXTYPE=dssp1-minimal
" > /etc/selinux/config

	ln -sf /etc/selinux/config /etc/sysconfig/selinux
	restorecon /etc/selinux/config 2> /dev/null || :
else
	. /etc/selinux/config
	[ "${SELINUXTYPE}" == "dssp1-minimal" ] && selinuxenabled && load_policy
fi
exit 0

%postun
if [ $1 = 0 ]; then
	setenforce 0 2> /dev/null
	if [ ! -s /etc/selinux/config ]; then
		echo "SELINUX=disabled" > /etc/selinux/config
	else
		sed -i 's/^SELINUX=.*/SELINUX=disabled/g' /etc/selinux/config
	fi
fi
exit 0

%triggerin -- pcre
selinuxenabled && semodule -nB

%changelog
* Tue Nov 15 2016 Dominick Grift <dac.override@gmail.com> - 1.0-%(date +%Y%%m%%d)git%{shortcommit0}
- Git snapshot
