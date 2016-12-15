.PHONY: all check clean policy install-config install-semodule

# Include the build configuration for the
# policy name and version.
include build.conf

BINDIR ?= /usr/bin
SBINDIR ?= /usr/sbin
DESTDIR ?=
SYSCONFDIR ?= /etc
SHAREDSTATEDIR ?= /var/lib
SECILC = $(BINDIR)/secilc
SEMODULE = $(SBINDIR)/semodule
MKDIR = $(BINDIR)/mkdir
INSTALL = $(BINDIR)/install

POLICY_CONFIG_SOURCES = config/customizable_types \
		  config/dbus_contexts \
		  config/default_contexts \
		  config/default_type \
		  config/failsafe_context \
		  config/media \
		  config/openssh_contexts \
		  config/removable_context \
		  config/securetty_types \
		  config/x_contexts

TARGET_LC = $(shell echo $(TARGET) | tr A-Z a-z)

ifeq ($(TARGET_LC), debian)
	POLICY_CONFIG_SOURCES += config/file_contexts.subs_dist.debian
	FILE_CONTEXTS_SUBS_DIST = config/file_contexts.subs_dist.debian
else
	POLICY_CONFIG_SOURCES += config/file_contexts.subs_dist
	FILE_CONTEXTS_SUBS_DIST = config/file_contexts.subs_dist
endif

BASE_POLICY_SOURCES = src/base/av.cil \
		  src/base/classmap.cil \
		  src/base/classpermission.cil \
		  src/base/cmd.cil \
		  src/base/config.cil \
		  src/base/dev.cil \
		  src/base/file.cil \
		  src/base/fs.cil \
		  src/base/isid.cil \
		  src/base/lib.cil \
		  src/base/model.cil \
		  src/base/net.cil \
		  src/base/pattern.cil \
		  src/base/polcap.cil \
		  src/base/sec.cil \
		  src/base/stor.cil \
		  src/base/subj.cil \
		  src/base/sys.cil \
		  src/base/template.cil \
		  src/base/term.cil

MINIMAL_POLICY_SOURCES = src/minimal.cil \
		  src/tunable.cil

all: clean policy.$(POLICY_VERSION)

clean:
	$(RM) policy.$(POLICY_VERSION) file_contexts

$(POLICY_VERSION): $(BASE_POLICY_SOURCES) $(MINIMAL_POLICY_SOURCES)
	$(SECILC) --policyvers=$(POLICY_VERSION) --o="$@" $^

policy.%: $(BASE_POLICY_SOURCES) $(MINIMAL_POLICY_SOURCES)
	$(SECILC) --policyvers=$* --o="$@" $^

install-config: $(POLICY_CONFIG_SOURCES)
	$(MKDIR) -p $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/logins
	$(MKDIR) -p $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/files
	$(MKDIR) -p $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/users
	$(INSTALL) -m0644 config/customizable_types $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/customizable_types
	$(INSTALL) -m0644 config/securetty_types $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/securetty_types
	$(INSTALL) -m0644 config/dbus_contexts $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/dbus_contexts
	$(INSTALL) -m0644 config/default_contexts $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/default_contexts
	$(INSTALL) -m0644 config/default_type $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/default_type
	$(INSTALL) -m0644 config/failsafe_context $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/failsafe_context
	$(INSTALL) -m0644 config/openssh_contexts $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/openssh_contexts
	$(INSTALL) -m0644 config/removable_context $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/removable_context
	$(INSTALL) -m0644 config/media $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/files/media
	$(INSTALL) -m0644 $(FILE_CONTEXTS_SUBS_DIST) $(DESTDIR)/$(SYSCONFDIR)/selinux/$(POLICY_NAME)/contexts/files/file_contexts.subs_dist

install-semodule: install-config $(BASE_POLICY_SOURCES) $(MINIMAL_POLICY_SOURCES)
	$(MKDIR) -p $(DESTDIR)/$(SHAREDSTATEDIR)/selinux/$(POLICY_NAME)
	$(SEMODULE) -p $(DESTDIR) --priority=100 -i $(BASE_POLICY_SOURCES) $(MINIMAL_POLICY_SOURCES) -N -s $(POLICY_NAME)

