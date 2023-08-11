#!/bin/bash

mkdir -p compiled images

for i in sources/*.txt tests/*.txt; do
	echo "Compiling: $i"
    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done


#A2R
echo "Creating the transducer A2R"
fstinvert compiled/R2A.fst > compiled/A2R.fst

#birthR2A
echo "Creating the transducer birthR2A"
fstcompose compiled/R2A.fst compiled/d2dd.fst > compiled/R2A_d2dd_composed.fst
fstcompose compiled/R2A.fst compiled/d2dddd.fst > compiled/R2A_d2dddd_composed.fst
fstconcat compiled/R2A_d2dd_composed.fst compiled/copy.fst > compiled/R2A_d2dd_composed_copy1.fst
fstconcat compiled/R2A_d2dd_composed_copy1.fst compiled/R2A_d2dd_composed.fst > compiled/R2A_d2dd_composed_copy2.fst
fstconcat compiled/R2A_d2dd_composed_copy2.fst compiled/copy.fst > compiled/R2A_d2dd_composed_copy3.fst
fstconcat compiled/R2A_d2dd_composed_copy3.fst compiled/R2A_d2dddd_composed.fst > compiled/birthR2A.fst
rm compiled/R2A_d2dd_composed.fst
rm compiled/R2A_d2dddd_composed.fst
rm compiled/R2A_d2dd_composed_copy1.fst
rm compiled/R2A_d2dd_composed_copy2.fst
rm compiled/R2A_d2dd_composed_copy3.fst

#birthA2T
echo "Creating the transducer birthA2T"
fstconcat compiled/d2dd.fst compiled/copy.fst > compiled/d2dd_copy.fst
fstconcat compiled/d2dd_copy.fst compiled/mm2mmm.fst > compiled/d2dd_copy1_mm2mmm.fst
fstconcat compiled/d2dd_copy1_mm2mmm.fst compiled/copy.fst > compiled/d2dd_copy2_mm2mmm.fst
fstconcat compiled/d2dd_copy2_mm2mmm.fst compiled/d2dddd.fst > compiled/birthA2T.fst
rm compiled/d2dd_copy.fst
rm compiled/d2dd_copy1_mm2mmm.fst
rm compiled/d2dd_copy2_mm2mmm.fst

#birthT2R
echo "Creating the transducer birthT2R"
fstinvert compiled/d2dd.fst > compiled/dd2d.fst
fstinvert compiled/mm2mmm.fst > compiled/mmm2mm.fst
fstinvert compiled/d2dddd.fst > compiled/dddd2d.fst
fstcompose compiled/dd2d.fst compiled/A2R.fst > compiled/A2R_dd2d_composed.fst
fstconcat compiled/A2R_dd2d_composed.fst compiled/copy.fst > compiled/A2R_dd2d_composed_copy.fst
fstcompose compiled/mmm2mm.fst compiled/dd2d.fst > compiled/dd2d_mmm2mm_composed.fst
fstcompose compiled/dd2d_mmm2mm_composed.fst compiled/A2R.fst > compiled/A2R_dd2d_mmm2mm_composed.fst
fstconcat compiled/A2R_dd2d_composed_copy.fst compiled/A2R_dd2d_mmm2mm_composed.fst > compiled/A2R_dd2d_composed_copy_mmm2mm1.fst
fstconcat compiled/A2R_dd2d_composed_copy_mmm2mm1.fst compiled/copy.fst > compiled/A2R_dd2d_composed_copy_mmm2mm2.fst
fstcompose compiled/dddd2d.fst compiled/A2R.fst > compiled/A2R_dddd2d_composed.fst
fstconcat compiled/A2R_dd2d_composed_copy_mmm2mm2.fst compiled/A2R_dddd2d_composed.fst > compiled/birthT2R.fst
rm compiled/dd2d.fst
rm compiled/mmm2mm.fst
rm compiled/dddd2d.fst
rm compiled/A2R_dd2d_composed.fst
rm compiled/A2R_dd2d_composed_copy.fst
rm compiled/dd2d_mmm2mm_composed.fst
rm compiled/A2R_dd2d_mmm2mm_composed.fst
rm compiled/A2R_dd2d_composed_copy_mmm2mm1.fst
rm compiled/A2R_dd2d_composed_copy_mmm2mm2.fst
rm compiled/A2R_dddd2d_composed.fst

#birthR2L
echo "Creating the transducer birthR2L"
fstcompose compiled/birthR2A.fst compiled/date2year.fst > compiled/birthR2A_date2_year_composed.fst
fstcompose compiled/birthR2A_date2_year_composed.fst compiled/leap.fst > compiled/birthR2L.fst
rm compiled/birthR2A_date2_year_composed.fst

echo "Testing the transducer birthR2A"
fstcompose "compiled/87668birthR2A.fst" "compiled/birthR2A.fst" > "compiled/87668birthR2ATestResult.fst" 

echo "Testing the transducer birthA2T"
fstcompose "compiled/87668birthA2T.fst" "compiled/birthA2T.fst" > "compiled/87668birthA2TTestResult.fst"

echo "Testing the transducer birthT2R"
fstcompose "compiled/87668birthT2R.fst" "compiled/birthT2R.fst" > "compiled/87668birthT2RTestResult.fst"

echo "Testing the transducer birthR2L"
fstcompose "compiled/87668birthR2L.fst" "compiled/birthR2L.fst" > "compiled/87668birthR2LTestResult.fst" 

for i in compiled/*.fst; do
	echo "Creating image: images/$(basename $i '.fst').pdf"
    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i '.fst').pdf
done