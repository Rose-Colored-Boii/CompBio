import sys
from chimerax.core.commands import run

model = run(session, "alphafold fetch " + sys.argv[1])
run(session, "show surface only")
run(session, "color bychain")
run(session, "save " + sys.argv[1] + ".glb")



