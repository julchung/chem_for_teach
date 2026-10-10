import { fetchMoleculeInfo } from './src/utils/pubchemApi';
(async () => {
  const result = await fetchMoleculeInfo('C=C([H])([H])([H])([H])');
  console.log(result);
})();
