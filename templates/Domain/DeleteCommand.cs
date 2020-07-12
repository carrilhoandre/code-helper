using NetDevPack.Messaging;
using System;

namespace {{projectNamespace}}.Domain.Commands.Inputs.Shared
{
    public class DeleteCommand : Command
    {
        public Guid Id { get; set; }
    }
}
