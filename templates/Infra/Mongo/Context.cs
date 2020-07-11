using MongoDB.Driver;
using NetDevPack.Data;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace {{projectNamespace}}.Infrastructure.MongoDb.Contexts
{
    public class {{dataContext}} : IUnitOfWork
    {
        private IMongoDatabase _database = null;
        private readonly string _connectionString;
        public MongoClient MongoClient { get; set; }
        private readonly List<Func<Task>> _commands;
        public IClientSessionHandle Session { get; set; }

        public {{dataContext}}(string connectionString)
        {
            _connectionString = connectionString;
            _commands = new List<Func<Task>>();
            MongoClient = new MongoClient(connectionString);
            if (MongoClient != null)
                _database = MongoClient.GetDatabase("{{databaseName}}");
        }

        public async Task<bool> SaveChangesAsync()
        {
            ConfigureMongo();

            using (Session = await MongoClient.StartSessionAsync())
            {
                Session.StartTransaction();

                var commandTasks = _commands.Select(c => c());

                await Task.WhenAll(commandTasks);

                await Session.CommitTransactionAsync();
            }

            return _commands.Count > 0;
        }

        public IMongoCollection<T> GetCollectionByType<T>()
        {
            return _database.GetCollection<T>(nameof(T));
        }

        public void AddCommand(Func<Task> func)
        {
            _commands.Add(func);
        }

        public IMongoCollection<T> GetCollection<T>(string name)
        {
            return _database.GetCollection<T>(name);
        }

        private void ConfigureMongo()
        {
            if (MongoClient != null)
                return;

            MongoClient = new MongoClient(_connectionString);
            if (MongoClient != null)
                _database = MongoClient.GetDatabase("{{databaseName}}");

        }

        public void Dispose()
        {
            Session?.Dispose();
            GC.SuppressFinalize(this);
        }

        public async Task<bool> Commit()
        {
            return await SaveChangesAsync();
        }
    }
}
