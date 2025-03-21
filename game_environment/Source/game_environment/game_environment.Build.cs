// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class game_environment : ModuleRules
{
	public game_environment(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "HeadMountedDisplay" });
	}
}
