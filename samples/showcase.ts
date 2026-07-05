// Crowquill Mono — showcase (Neovide)
// keywords ficam bold+coral sozinhas | ligaduras: => -> != >= <= === !== |> ??
// fronteira de palavra: constante / myconst / returned / iffy NAO bolda.

import { readFile } from "node:fs/promises";
import type { Result } from "./types";

const MAX_RETRIES = 3;
let counter = 0;

export async function fetchUser(id: number): Promise<Result<User>> {
  for (let i = 0; i < MAX_RETRIES; i++) {
    try {
      const res = await fetch(`/api/users/${id}`);
      if (res.status === 200 && res.ok !== false) {
        return { ok: true, value: (await res.json()) as User };
      }
    } catch (err) {
      if (i >= MAX_RETRIES - 1) throw err;
      continue;
    }
  }
  return { ok: false, error: "unreachable" };
}

interface User {
  readonly id: number;
  name: string;
  roles: ("admin" | "user")[];
}

type Predicate<T> = (x: T) => boolean;

const isAdmin: Predicate<User> = (u) =>
  u.roles.includes("admin") && u.id !== 0;

class Cache<K, V> {
  private store = new Map<K, V>();
  get(k: K): V | undefined {
    return this.store.get(k);
  }
  set(k: K, v: V): this {
    this.store.set(k, v);
    return this;
  }
}

export default async function main() {
  const cache = new Cache<number, User>();
  const result = await fetchUser(42);
  switch (result.ok) {
    case true:
      cache.set(result.value.id, result.value);
      break;
    default:
      console.error(result.error);
  }
  // estes NAO devem ficar bold (nao sao a palavra inteira):
  const constante = 1, myconst = 2, returned = 3, iffy = 4, none = 5;
  return constante + myconst + returned + iffy + none;
}
