using NetDevPack.Data;
using NetDevPack.Domain;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{projectNamespace}}.Domain.Repositories
{
    public interface IBaseRepository<TEntity> : IRepository<TEntity> where TEntity : IAggregateRoot
    {
        void Add(TEntity obj);
        Task<TEntity> GetById(Guid id);
        Task<IEnumerable<TEntity>> GetAll();
        void Update(TEntity obj);
        void Remove(Guid id);
    }
}
