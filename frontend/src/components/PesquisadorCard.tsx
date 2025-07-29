interface Pesquisador {
  nome: string;
  id_lattes: string;
  resumo: string;
}

interface PesquisadorCardProps {
  pesquisador: Pesquisador;
}

const PesquisadorCard = ({ pesquisador }: PesquisadorCardProps) => {
  return (
    <div className="bg-card border border-border rounded-lg p-6 shadow-sm hover:shadow-md transition-shadow">
      <h3 className="font-bold text-lg text-foreground mb-2">
        {pesquisador.nome}
      </h3>
      <p className="text-sm text-muted-foreground mb-3">
        <span className="font-medium">ID Lattes:</span> {pesquisador.id_lattes}
      </p>
      <p className="text-sm text-foreground line-clamp-3">
        {pesquisador.resumo}
      </p>
    </div>
  );
};

export default PesquisadorCard;