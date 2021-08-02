using {{ProjectNamespace}}.Domain.Models;
using {{ProjectNamespace}}.Domain.Results.{{plural}};
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{ProjectNamespace}}.Domain.Repositories
{
    public interface I{{EntityName}}Repository : IBaseRepository<{{EntityName}}>
    {
        Task<IEnumerable<{{EntityName}}Result>> List();
    }
}
