using NetDevPack.Data;
using NetDevPack.Domain;
using System;
using System.Collections.Generic;
using System.Threading;
using System.Threading.Tasks;

namespace {{ProjectNamespace}}.Domain.Repositories
{
    public interface IBaseRepository<TEntity> : IRepository<TEntity> where TEntity : IAggregateRoot
    {
        void Add(TEntity obj);
        Task<TEntity> GetByIdAsync(Guid id, CancellationToken cancellationToken = default);
        Task<IEnumerable<TEntity>> GetAllAsync(CancellationToken cancellationToken = default);
        void Update(TEntity obj);
        void Remove(Guid id);
    }
}
