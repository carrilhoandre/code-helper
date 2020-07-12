using {{projectNamespace}}.Domain.Models;
using {{projectNamespace}}.Domain.Results.{{plural}};
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{projectNamespace}}.Domain.Repositories
{
    public interface I{{className}}Repository : IBaseRepository<{{className}}>
    {
        Task<IEnumerable<{{className}}Result>> List();
    }
}
