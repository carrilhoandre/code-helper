using {{projectNamespace}}.Domain.Models;
using {{projectNamespace}}.Domain.Repositories;
using {{projectNamespace}}.Infrastructure.MongoDb.Contexts;
using MongoDB.Driver;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{projectNamespace}}.Infrastructure.MongoDb.Repositories
{
    public class {{ className }}Repository : BaseRepository<{{ className }}>, I{{ className }}Repository
    {
        public {{ className }}Repository(CrudContext crudContext) : base(crudContext)
        {
        }
    }
}
