TARGET := py_ser_freeastro

PYSRCS := setup.py
PYSRCS += ./py_ser_freeastro/core.py
PYSRCS += ./py_ser_freeastro/version.py
PYSRCS += ./py_ser_freeastro/__init__.py

README += README.md

VERB := @

all: py_ser_freeastro/core.py ctags
	$(VERB)python3 $< ASICAP_2019-05-05_01_46_42_235.SER

dist:
	$(VERB)python3 setup.py sdist bdist

vim: ctags
# 	$(VERB)source ../bin/activate
	$(VERB)echo vim Makefile $(PYSRCS) $(README)
# 	deactivate

CTAGS = ctags
CTAGSFLAGS = -h ".py" --python-kinds=-i

ctags:
	$(VERB)$(CTAGS) $(CTAGSFLAGS) $(PYSRCS)

show:
	$(VERB)echo "TARGET:     " $(TARGET)
	$(VERB)echo "PYSRCS:     " $(PYSRCS)
	$(VERB)echo "VERB:       " $(VERB)
	$(VERB)echo "CTAGS:      " $(CTAGS)
	$(VERB)echo "CTAGSFLAGS: " $(CTAGSFLAGS)
	$(VERB)echo "README:     " $(README)

.PHONY: dist
