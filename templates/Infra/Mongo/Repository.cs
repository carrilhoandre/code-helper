using {{ProjectNamespace}}.Domain.Models;
using {{ProjectNamespace}}.Domain.Repositories;
using {{ProjectNamespace}}.Infrastructure.MongoDb.Contexts;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{ProjectNamespace}}.Infrastructure.MongoDb.Repositories
{
    public class {{ className }}Repository : BaseRepository<{{ className }}>, I{{ className }}Repository
    {
        public {{ className }}Repository(CrudContext crudContext) : base(crudContext)
        {
        }
    }
}
