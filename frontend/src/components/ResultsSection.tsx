import PesquisadorCard from './PesquisadorCard';
import ArtigoCard from './ArtigoCard';
import LoadingSpinner from './LoadingSpinner';
import { AlertCircle } from 'lucide-react';

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

interface ResultsSectionProps {
  isLoading: boolean;
  pesquisadores: Pesquisador[];
  artigos: Artigo[];
  hasSearched: boolean;
  error: string | null;
}

const ResultsSection = ({ 
  isLoading, 
  pesquisadores, 
  artigos, 
  hasSearched, 
  error 
}: ResultsSectionProps) => {
  if (!hasSearched) {
    return (
      <section className="text-center py-12">
        <p className="text-muted-foreground text-lg">
          Digite um termo e clique em buscar para ver os resultados.
        </p>
      </section>
    );
  }

  if (isLoading) {
    return (
      <section>
        <LoadingSpinner />
      </section>
    );
  }

  if (error) {
    return (
      <section className="text-center py-12">
        <AlertCircle className="w-12 h-12 text-destructive mx-auto mb-4" />
        <p className="text-destructive text-lg">
          Erro ao buscar resultados: {error}
        </p>
      </section>
    );
  }

  const hasResults = pesquisadores.length > 0 || artigos.length > 0;

  if (!hasResults) {
    return (
      <section className="text-center py-12">
        <p className="text-muted-foreground text-lg">
          Nenhum resultado encontrado para o termo buscado.
        </p>
      </section>
    );
  }

  return (
    <section className="space-y-8">
      {pesquisadores.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold text-foreground mb-6">
            Pesquisadores Encontrados
          </h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {pesquisadores.map((pesquisador, index) => (
              <PesquisadorCard key={index} pesquisador={pesquisador} />
            ))}
          </div>
        </div>
      )}

      {artigos.length > 0 && (
        <div>
          <h2 className="text-2xl font-bold text-foreground mb-6">
            Artigos Encontrados
          </h2>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {artigos.map((artigo, index) => (
              <ArtigoCard key={index} artigo={artigo} />
            ))}
          </div>
        </div>
      )}
    </section>
  );
};

export default ResultsSection;