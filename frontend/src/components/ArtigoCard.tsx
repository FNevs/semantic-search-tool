interface Artigo {
  titulo: string;
  ano: string;
  doi: string;
}

interface ArtigoCardProps {
  artigo: Artigo;
}

const ArtigoCard = ({ artigo }: ArtigoCardProps) => {
  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="font-bold text-lg text-foreground mb-2">
        {artigo.titulo}
      </h3>
      <p className="text-sm text-muted-foreground mb-2">
        <span className="font-medium">Ano:</span> {artigo.ano}
      </p>
      <p className="text-sm text-muted-foreground">
        <span className="font-medium">DOI:</span> {artigo.doi}
      </p>
    </div>
  );
};

export default ArtigoCard;