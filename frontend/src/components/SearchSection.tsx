import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Search } from 'lucide-react';

interface SearchSectionProps {
  onSearch: (term: string) => void;
  isLoading: boolean;
}

const SearchSection = ({ onSearch, isLoading }: SearchSectionProps) => {
  const [searchTerm, setSearchTerm] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (searchTerm.trim()) {
      onSearch(searchTerm.trim());
    }
  };

  return (
    <section className="mb-8">
      <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4 max-w-2xl mx-auto">
        <Input
          type="text"
          placeholder="Digite um nome de pesquisador ou termo do artigo..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="flex-1 h-12 text-base"
          disabled={isLoading}
        />
        <Button 
          type="submit" 
          className="h-12 px-8 text-base"
          disabled={isLoading || !searchTerm.trim()}
        >
          <Search className="w-4 h-4 mr-2" />
          Buscar
        </Button>
      </form>
    </section>
  );
};

export default SearchSection;