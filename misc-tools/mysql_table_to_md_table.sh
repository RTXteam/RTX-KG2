sed -i -E "s/\+(-)+/\|--/g" umls_table.txt
sed -i -E "s/^\|( )*//g" umls_table.txt
sed -i -E "s/--\+$/--/g" umls_table.txt
sed -i -E "s/( )+/ /g" umls_table.txt
sed -i -E "s/<|>//g" umls_table.txt
