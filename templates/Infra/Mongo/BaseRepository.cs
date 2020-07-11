using {{projectName}}.Domain.Repositories;
using {{projectName}}.Infrastructure.MongoDb.Contexts;
using MongoDB.Driver;
using NetDevPack.Data;
using NetDevPack.Domain;
using ServiceStack;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace {{projectName}}.Infrastructure.MongoDb.Repositories
{
    public class BaseRepository<TEntity> : IBaseRepository<TEntity> where TEntity : IAggregateRoot
    {
        protected CrudContext Context = null;
        protected IMongoCollection<TEntity> DbSet;

        public IUnitOfWork UnitOfWork => Context;

        public BaseRepository(CrudContext crudContext)
        {
            Context = crudContext;
            ConfigDbSet();
        }

        public virtual void Add(TEntity obj)
        {
            Context.AddCommand(() => DbSet.InsertOneAsync(obj));
        }

        private void ConfigDbSet()
        {
            DbSet = Context.GetCollection<TEntity>(typeof(TEntity).Name);
        }

        public virtual async Task<TEntity> GetById(Guid id)
        {
            var data = await DbSet.FindAsync(Builders<TEntity>.Filter.Eq("_id", id));
            return data.SingleOrDefault();
        }

        public virtual async Task<IEnumerable<TEntity>> GetAll()
        {
            var all = await DbSet.FindAsync(Builders<TEntity>.Filter.Empty);
            return all.ToList();
        }

        public virtual void Update(TEntity obj)
        {
            Context.AddCommand(() => DbSet.ReplaceOneAsync(Builders<TEntity>.Filter.Eq("_id", obj.GetId()), obj));
        }

        public virtual void Remove(Guid id)
        {
            Context.AddCommand(() => DbSet.DeleteOneAsync(Builders<TEntity>.Filter.Eq("_id", id)));
        }

        public void Dispose()
        {
            Context?.Dispose();
        }
    }
}
