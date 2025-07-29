import { useState } from 'react';
import Header from '@/components/Header';
import SearchSection from '@/components/SearchSection';
import ResultsSection from '@/components/ResultsSection';
import { useToast } from '@/hooks/use-toast';

interface Pesquisador {
  nome: string;
  id_lattes: string;
  resumo: string;
}

interface Artigo {
  titulo: string;
  ano: string;
  doi: string;
}

const Index = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [pesquisadores, setPesquisadores] = useState<Pesquisador[]>([]);
  const [artigos, setArtigos] = useState<Artigo[]>([]);
  const [hasSearched, setHasSearched] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleSearch = async (term: string) => {
    setIsLoading(true);
    setError(null);
    setHasSearched(true);
    
    try {
      const [pesquisadoresResponse, artigosResponse] = await Promise.all([
        fetch(`http://localhost:8000/pesquisadores/textual/${encodeURIComponent(term)}`),
        fetch(`http://localhost:8000/artigos/textual/${encodeURIComponent(term)}`)
      ]);

      if (!pesquisadoresResponse.ok || !artigosResponse.ok) {
        throw new Error('Erro ao conectar com a API');
      }

      const pesquisadoresData = await pesquisadoresResponse.json();
      const artigosData = await artigosResponse.json();

      setPesquisadores(pesquisadoresData);
      setArtigos(artigosData);

      toast({
        title: "Busca concluída",
        description: `Encontrados ${pesquisadoresData.length} pesquisadores e ${artigosData.length} artigos`,
      });

    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Erro desconhecido';
      setError(errorMessage);
      setPesquisadores([]);
      setArtigos([]);
      
      toast({
        title: "Erro na busca",
        description: "Verifique se a API está rodando em http://localhost:8000",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        <Header />
        <SearchSection onSearch={handleSearch} isLoading={isLoading} />
        <ResultsSection
          isLoading={isLoading}
          pesquisadores={pesquisadores}
          artigos={artigos}
          hasSearched={hasSearched}
          error={error}
        />
      </div>
    </div>
  );
};

export default Index;