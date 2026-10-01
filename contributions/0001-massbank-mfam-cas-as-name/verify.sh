#!/usr/bin/env bash
# Reproduce every check behind contribution 0001. Needs: python3 + rdkit,
# Java 21, OPSIN 2.9.0 jar, MassBank-cli-tools v1.3.0.
#   OPSIN_JAR=... MBCLI=.../MassBank-cli-tools JAVA=java ./verify.sh
set -euo pipefail
cd "$(dirname "$0")"
JAVA=${JAVA:-java}
echo "1. Names -> structure (OPSIN): first InChIKey block must equal the record's"
printf "Methyl indole-3-acetate\n2'-Deoxycytidine 5'-monophosphate\n2-(Glucopyranosyloxy)benzoic acid\n" \
  | $JAVA -jar "$OPSIN_JAR" -o stdinchikey 2>/dev/null \
  | paste - <(printf "KTHADMDGDNYQRX\nNCMVOABPESMRCP\nTZPBMNKOLMSJPF\n") \
  | awk '{split($1,a,"-"); print "   " $1, (a[1]==$2 ? "MATCH" : "MISMATCH"); if (a[1]!=$2) bad=1} END {exit bad}'
echo "2. CAS check digits"
python3 -c "
for c in ['1912-33-0','1032-65-1','10366-91-3']:
    a,b,k=c.split('-'); d=(a+b)[::-1]
    ok=sum((i+1)*int(x) for i,x in enumerate(d))%10==int(k); print('  ',c,'valid' if ok else 'INVALID'); assert ok"
echo "3. Record self-consistency (RDKit): SMILES -> InChIKey and formula"
python3 - <<'PY'
import glob,re
from rdkit import Chem,RDLogger; from rdkit.Chem import inchi,rdMolDescriptors
RDLogger.DisableLog('rdApp.*')
for f in sorted(glob.glob("patched/*.txt")):
    t=open(f).read(); g=lambda k: re.search(rf"^{re.escape(k)}(.*)$",t,re.M).group(1).strip()
    m=Chem.MolFromSmiles(g("CH$SMILES: "))
    assert inchi.MolToInchiKey(m)==g("CH$LINK: INCHIKEY "), f
    assert rdMolDescriptors.CalcMolFormula(m)==g("CH$FORMULA: "), f
    print("  ",f,"ok")
PY
echo "4. MassBank Validator (the check upstream CI runs)"
$JAVA ${JAVA_OPTS:-} -jar "$MBCLI/lib/Validator.jar" patched/*.txt
echo "all checks passed"
