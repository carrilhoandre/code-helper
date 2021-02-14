using {{ProjectNamespace}}.Domain.Models;
using {{ProjectNamespace}}.Domain.Results.{{plural}};
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{ProjectNamespace}}.Domain.Repositories
{
    public interface I{{className}}Repository : IBaseRepository<{{className}}>
    {
        Task<IEnumerable<{{className}}Result>> List();
    }
}
