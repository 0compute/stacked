MAKEENV_VERSION = master
MAKEENV_ROOT = .makeenv-$(MAKEENV_VERSION)
MAKEENV_CORE = $(MAKEENV_ROOT)/makeenv.mak
ifeq ($(wildcard $(MAKEENV_CORE)),)
CURL ?= curl --fail --location
_BOOTSTRAP = mkdir -p $(MAKEENV_ROOT) && $(CURL) \
	https://github.com/0compute/makeenv/archive/$(MAKEENV_VERSION).tar.gz \
	| tar -C $(MAKEENV_ROOT) --strip-components=1 -xz
$(if $(shell (echo "$(_BOOTSTRAP)" && $(_BOOTSTRAP)) 1>&2 || echo x), \
	$(error Could not bootstrap makeenv))
endif
include $(MAKEENV_CORE)
